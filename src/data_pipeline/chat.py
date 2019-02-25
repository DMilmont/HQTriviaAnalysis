import platform
import re
from datetime import datetime

from config import readFromConfig, writeToFile

import sqlite3

conn = sqlite3.connect('HQInsiders.db')
c = conn.cursor()

showID = int(datetime.now().strftime('%m%d%y%H'))

class Chat(object):
    def __init__(self):
        self.enable = readFromConfig("Chat", "enable")
        self.show_kicked = readFromConfig("Chat", "show_kicked")
        self.show_message = readFromConfig("Chat", "show_message")
        self.show_usernames = readFromConfig("Chat", "show_usernames")
        self.show_userids = readFromConfig("Chat", "show_userids")

    def showMessage(self, message):
        if not self.enable:
            return True
            
        return True

    def prepareMessage(self):

        userID = str(self.message["metadata"]["userId"])
        userName = str(self.message["metadata"]["username"])
        chatMessage = str(self.message["metadata"]["message"])

        try:
            c.execute("INSERT INTO chats (showID, userID, userName, chatMessage, chatTime) VALUES (?, ?, ?, ?, ?)",
                (showID, userID, userName, chatMessage, str(datetime.now())))
            conn.commit()
        except (Exception) as e:
            print('insert did not work for chat!',e)

        return True

