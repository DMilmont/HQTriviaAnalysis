import os
import csv

from configparser import ConfigParser

configFile = ConfigParser()
configFile.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))

try:
    login_header = {
        "Authorization": "Bearer " + configFile["Login"]["authorization_key"],
        "x-hq-client": configFile["General"]["hq_client"]
    }
except:
    login_header = {}


def readFromConfig(section, parameter):
    value = configFile[section][parameter]

    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        return value

def writeToFile(type,data):
     if type == 'chat':
         with open('chats.txt', 'w') as c: 
             c.write('userId,userName,message,dateTime')
             writer = csv.writer(c)
             writer.writerow(data)
             #writeToFile('chat',[str(self.message["metadata"]["userId"]),str(self.message["metadata"]["username"]),str(self.message["metadata"]["message"]),str(datetime.now())])
     elif type == 'question':
         with open('questions.txt', 'w') as q: 
             q.write('questionId,questionNumber,category,question,dateTime')
             writer = csv.writer(q)
             writer.writerow(data)
             #writeToFile('question',[str(self.question["questionId"]),str(self.question["questionNumber"]), str(self.question["category"]), str(self.question["question"]),str(datetime.now())])
     elif type == 'answer':
         with open('answers.txt', 'w') as f: 
             f.write('questionId,answerText,isCorrect,count,dateTime')
             writer = csv.writer(f)
             writer.writerow(data)
             #writeToFile('answer',[str(self.question["questionId"]),answerText,isCorrect,count,str(datetime.now())])
     else: 
          print('unknown type for')


