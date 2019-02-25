import json
import requests
import sys

from config import login_header, readFromConfig
from shutil import get_terminal_size
from datetime import datetime

from autobahn.twisted.websocket import connectWS
from twisted.internet import reactor, ssl

from game import GameFactory

import sqlite3

conn = sqlite3.connect('HQInsiders.db')
c = conn.cursor()


class Launcher(object):
    def __init__(self):
        self.api_shows = readFromConfig("API", "shows_now")
        self.debug = readFromConfig("General", "debug_mode")
        self.server_ip = readFromConfig("General", "server_ip")

    def launchDataConsumption(self):

        print(" HQ Trivia Data Consumption Started ".center(get_terminal_size()[0], "="))

        if self.showAlive():
            socketURL = self.getSocketURL()

            proto = socketURL.split('://')[0]
            server = socketURL.split('://')[1].split("/")[0]
            server_dir = socketURL.replace(proto + '://' + server, "")

            if proto == "http":
                self.socketURL = "ws://" + server + ":80" + server_dir
            elif proto == "https":
                self.socketURL = "wss://" + server + ":443" + server_dir
            else:
                self.socketURL = socketURL

            factory = GameFactory(self.socketURL, headers=login_header)
            factory.setProtocolOptions(autoPingInterval=5, autoPingTimeout=5, autoPingSize=20)

            if factory.isSecure:
                contextFactory = ssl.ClientContextFactory()
            else:
                contextFactory = None

            connectWS(factory, contextFactory)
            reactor.run()
        else:
            print(''.center(get_terminal_size()[0], '='))
            sys.exit(0)

    def showAlive(self):
        """ Checks if show is live """

        request = requests.get(self.server_ip + self.api_shows, headers=login_header)
        response = request.content.decode()

        try:
            responseJSON = json.loads(response)
            showID = int(datetime.now().strftime('%m%d%y%H'))

            if responseJSON["active"]:
                try:
                    c.execute("INSERT INTO cronLog (showID, programMessage, broadcastTime) VALUES (?, ?, ?)",
                    (showID, "show is live, program is running!", str(datetime.now())))
                    conn.commit()
                except (Exception) as e:
                    print('cron log insert did not work!',e)
            else:
                try:
                    c.execute("INSERT INTO cronLog (showID, programMessage, broadcastTime) VALUES (?, ?, ?)",
                    (showID, "show is not live, program is shutting down!", str(datetime.now())))
                    conn.commit()
                except (Exception) as e:
                    print('cron log insert did not work!',e)

            if responseJSON["active"]:
                print("Show is now live!".center(get_terminal_size()[0]))
                return True
            else:
                print("Show is not live!".center(get_terminal_size()[0]))
                return False
        except:
            print("Server returned unknown response!".center(get_terminal_size()[0]))
            print(responseJSON)
            return False

    def getSocketURL(self):

        request = requests.get(self.server_ip + self.api_shows, headers=login_header)
        response = request.content.decode()

        try:
            broadcastJSON = json.loads(response)["broadcast"]

            socketURL = broadcastJSON["socketUrl"]
            return socketURL
        except:
            return False


if __name__ == "__main__":
    Launcher().launchDataConsumption()
