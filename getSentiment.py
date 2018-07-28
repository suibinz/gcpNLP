#!/usr/bin/python

import subprocess
from google.cloud import language
import collections
import os, json
#import mysql.connector

client = language.LanguageServiceClient()
#db_conn = mysql.connector(user='onstak', password='Onstak123',
#                              host='127.0.0.1',
#                              database='devita')

def get_comments_from_db(db_conn):
	pass

def get_sent_score(comment, sentimentDict):
	document = language.types.Document( content = comment, type = "PLAIN_TEXT")
	response = client.analyze_sentiment( document = document, encoding_type = "UTF32")
	sent_score = response.document_sentiment.score

	if sent_score <= -0.6:
		sentimentDict["Highly_Neg"] += 1
	elif sent_score <= -0.2 and sent_score > -0.6:
		sentimentDict["Moderately_Neg"] += 1
	elif sent_score <= 0.2 and sent_score > -0.2:
		sentimentDict["Neutral"] += 1
	elif sent_score <= 0.6 and sent_score > 0.2:
		sentimentDict["Moderately_Pos"] += 1
	else: 
		sentimentDict["Highly_Pos"] += 1

def write_score():
    sentimentDict = collections.OrderedDict(
        {       "Highly_Neg": 0,
                "Moderately_Neg": 0,
                "Neutral": 0,
                "Moderately_Pos": 0,
                "Highly_Pos": 0
        })
    comments = []

    with open("comments", "r") as f:
        for line in f:
            comments.append(line)

    for comment in comments:
        get_sent_score(comment, sentimentDict)
        with open("./result/scores.json", "w") as  f:
            f.write(json.dumps(sentimentDict))

if __name__ == "__main__":
    write_score()
