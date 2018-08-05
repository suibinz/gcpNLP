#!/usr/bin/python

import subprocess
from google.cloud import language
import collections
import os, json
import _mysql
#import mysql.connector

client = language.LanguageServiceClient()
#db_conn = mysql.connector(user='onstak', password='Onstak123',
#                              host='127.0.0.1',
#                              database='devita')
DB_host = "172.16.174.41"
DB_user = "admin"
DB_passwd = "Onstak123"
DB_db = "acmedb"
DB_comments = "comment_content"
DB_table = "wp_comments"
DB_query = "SELECT " + DB_comments + " FROM " + "wp_comments"
comment_filename = "comment_from_db"

def get_comments_from_db():
    db = _mysql.connect(host=DB_host, user = DB_user, passwd = DB_passwd, db = DB_db)

    db.query(DB_query)
    results = db.use_result()

    with open(comment_filename, "w") as f:
        while True:
            comment = results.fetch_row()
            if any(comment):
                f.write(str(comment[0][0]).split("'")[1] + "\n")
            else:
                break

def get_sent_score(comment, sentimentDict):
	try:
		document = language.types.Document( content = comment, type = "PLAIN_TEXT")
		response = client.analyze_sentiment( document = document, encoding_type = "UTF32")
		sent_score = response.document_sentiment.score
	
		if sent_score <= -0.6:
			sentimentDict["Highly_Neg"] += 1
			sentimentDict["Poor_sent"] = comment
		elif sent_score <= -0.2 and sent_score > -0.6:
			sentimentDict["Moderately_Neg"] += 1
		elif sent_score <= 0.2 and sent_score > -0.2:
			sentimentDict["Neutral"] += 1
			sentimentDict["OK_sent"] = comment
		elif sent_score <= 0.6 and sent_score > 0.2:
			sentimentDict["Moderately_Pos"] += 1
		else: 
			sentimentDict["Highly_Pos"] += 1
			sentimentDict["Hi_sent"] = comment
	except:
		print("Language is not supported")

def write_score():
    sentimentDict = collections.OrderedDict(
        {       "Highly_Neg": 0,
                "Moderately_Neg": 0,
                "Neutral": 0,
                "Moderately_Pos": 0,
                "Highly_Pos": 0,
				"Poor_sent": '',
				"OK_sent": '',
				"Hi_sent": ''
        })
    comments = []

    with open(comment_filename, "r") as f:
        for line in f:
            comments.append(line)

    for comment in comments:
        get_sent_score(comment, sentimentDict)
        with open("./result/scores.json", "w") as  f:
            f.write(json.dumps(sentimentDict))

def runSentiment():
    get_comments_from_db()
    write_score()
