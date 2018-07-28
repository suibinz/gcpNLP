#!/usr/bin/python

import subprocess
from google.cloud import language
import collections
import os, json
#import mysql.connector


sentimentDict = collections.OrderedDict(
	{	"Highly_Neg": 0, 
		"Moderately_Neg": 0, 
		"Neutral": 0, 
		"Moderately_Pos": 0, 
		"Highly_Pos": 0
	})

client = language.LanguageServiceClient()
comments = []
#db_conn = mysql.connector(user='onstak', password='Onstak123',
#                              host='127.0.0.1',
#                              database='devita')

with open("comments", "r") as f:
	for line in f:
		comments.append(line)

def get_comments_from_db(db_conn):
	pass

def get_sent_score(comment):
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
    for comment in comments:
        get_sent_score(comment)
        with open("./result/scores.json", "w+") as  f:
            f.write(json.dumps(sentimentDict))

if __name__ == "__main__":
    for comment in comments:
        get_sent_score(comment)
        with open("./result/scores.json", "w+") as  f:
            f.write(json.dumps(sentimentDict))
