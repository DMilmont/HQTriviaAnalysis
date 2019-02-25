import json
import sys

from chat import Chat
from config import readFromConfig, writeToFile
from dataclasses import Data
from datetime import datetime
import csv

from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
from shutil import get_terminal_size
from twisted.internet.protocol import ReconnectingClientFactory

import sqlite3

conn = sqlite3.connect('HQInsiders.db')
c = conn.cursor()

showID = int(datetime.now().strftime('%m%d%y%H'))

debug = readFromConfig("General", "debug_mode")


class GameProtocol(WebSocketClientProtocol):
    def onOpen(self):
        if debug:
            print("[Connection] Connection established!")
        self.block_chat = False  # It will block chat when questions are shown
        self.chat = Chat()

        """ Broadcast Stats """
        self.bs_enable = readFromConfig("BroadcastStats", "enable")
        self.bs_connected = readFromConfig("BroadcastStats", "show_connected")
        self.bs_playing = readFromConfig("BroadcastStats", "show_playing")
        self.bs_eliminated = readFromConfig("BroadcastStats", "show_eliminated")

        """ Game Summary """
        self.gs_enable = readFromConfig("GameSummary", "enable")
        self.gs_prize = readFromConfig("GameSummary", "show_prize")
        self.gs_userids = readFromConfig("GameSummary", "show_userids")
        self.gs_usernames = readFromConfig("GameSummary", "show_usernames")

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = json.loads(payload.decode())

            #added to inspect JSON
            try:
                if (message["type"] != "interaction" and message["itemId"] != "chat") or message["type"] != "kicked":
                    with open('message.txt', 'w') as outfile:
                        json.dump(message, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
            except:
                print("count not write JSON summary file!!")

            if message["type"] == "question":
                self.block_chat = True 
                self.question = message   
                
                answers = self.question["answers"]
                category = self.question["category"]
                question = self.question["question"]
                questionID = int(self.question["questionId"])
                questionNumber = int(self.question["questionNumber"])

                # Inserting question data into the DB
                try:
                    c.execute("INSERT INTO questions (showID, questionID, questionNumber, category, question, questionTime) VALUES (?, ?, ?, ?, ?, ?)",
                        (showID, questionID, questionNumber, category, question, str(datetime.now())))
                    conn.commit()
                except:
                    print('insert did not work for question')

            elif message["type"] == "questionClosed":
                self.block_chat = False
            elif message["type"] == "questionSummary":
                self.block_chat = True 
                questionID = int(self.question["questionId"])
                answers = self.question["answerCounts"]
                answersCount = len(answers)

                for answer in range(answersCount):
                    answerText = str(answers[answer]["answer"])
                    isCorrect = str(answers[answer]["correct"])
                    count = str(answers[answer]["count"])
                    answerId = str(answers[answer]["answerId"])

                #inserting answer data into db
                try:
                    c.execute("INSERT INTO answers (showID, questionID, answerText, isCorrect, count, answerTime) VALUES (?, ?, ?, ?, ?, ?)",
                    (showID, questionID, answerText, isCorrect, count, str(datetime.now())))
                    
                    conn.commit()
                except:
                    print('insert did not work for question')

            elif message["type"] == "questionFinished":
                self.block_chat = False
  

            if not self.block_chat:
                if message["type"] == "broadcastStats" and self.bs_enable:
                    connected = str(message["viewerCounts"]["connected"])
                    playing = str(message["viewerCounts"]["playing"])
                    watching = str(message["viewerCounts"]["watching"])
                    
                    try:
                        c.execute("INSERT INTO broadcast_stats (showID, connected, playing, watching, broadcastTime) VALUES (?, ?, ?, ?, ?)",
                        (showID, connected, playing, watching, str(datetime.now())))
                        conn.commit()
                    except (Exception) as e:
                        print('insert did not work for broadcast stats!',e)

            if message["type"] == "gameSummary":
                
                try:
                    with open('gameSummary.txt', 'w') as outfile:
                        json.dump(message, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
                except:
                    print("can not write game summary JSON file!!")
                
                if self.gs_enable:
                    self.block_chat = True

                    winnings = 0.0
                    winnerCount = str(message["numWinners"])
                    winnerList = message["winners"]

                    print(" Game Summary ".center(get_terminal_size()[0], "="))
                    print((winnerCount + " Winners!").center(get_terminal_size()[0]))

                    for winner in range(len(winnerList)):
                        userInfo = winnerList[winner]

                        try:
                            cleanWinnings = userInfo["prize"].replace("$","")
                            cleanWinnings = cleanWinnings.replace(",","")
                            winnings += float(cleanWinnings)
                            print("winnings currently at: " + str(winnings))
                        except:
                            print("looks like winnings doesn't work!")

                        try:
                            c.execute("INSERT INTO payouts (showID, userID, userName, prize, broadcastTime) VALUES (?, ?, ?, ?, ?)",
                                (showID, str(userInfo["id"]), str(userInfo["name"]), str(userInfo["prize"]), str(datetime.now())))
                            conn.commit()
                        except (Exception) as e:
                            print('insert did not work for chat!',e)
            
            elif message["type"] == "postGame":
                self.block_chat = False
                try:
                    with open('postgame.txt', 'w') as outfile:
                        json.dump(message, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
                except:
                    print("could not write postgame JSON file!!")

            if message["type"] == "broadcastEnded":
                Data.allowReconnecting = False
                self.transport.loseConnection()


class GameFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = GameProtocol

    def clientConnectionFailed(self, connector, reason):
        if debug:
            print("[Connection] Connection failed! Retrying...")
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        if Data.allowReconnecting:
            if debug:
                print("[Connection] Connection has been lost! Retrying...")
            self.retry(connector)
        else:
            print(" Game Ended! ".center(get_terminal_size()[0], "*"))
