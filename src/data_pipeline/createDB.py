
import sqlite3

conn = sqlite3.connect('HQInsiders.db')
c = conn.cursor()

#create chat table
c.execute('''CREATE TABLE IF NOT EXISTS chats
    (userID integer, userName text, chatMessage text, chatTime text)''')
conn.commit()

#create question table
c.execute('''CREATE TABLE IF NOT EXISTS questions
    (questionID integer, questionNumber integer, category text, question text, questionTime text)''')
conn.commit()

#create answer table
c.execute('''CREATE TABLE IF NOT EXISTS answers
    (questionID integer, answerText text, isCorrect boolean, count integer, answerTime text)''')
conn.commit()

#create broadcast stats table
c.execute('''CREATE TABLE IF NOT EXISTS broadcast_stats
    (showID integer, connected text, playing text, watching text, broadcastTime text)''')
conn.commit()

#create payout table
c.execute('''CREATE TABLE IF NOT EXISTS payouts
    (showID integer, userID integer, userName text, prize float, broadcastTime text)''')
conn.commit()

#create cronLog table
c.execute('''CREATE TABLE IF NOT EXISTS cronLog
    (showID integer, programMessage text, broadcastTime text)''')
conn.commit()
conn.close()
