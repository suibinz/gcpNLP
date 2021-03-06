#!/usr/bin/python
import os
import json
import getSentiment
from flask import Flask, render_template, send_from_directory
app = Flask(__name__)

@app.route("/scores")
def template_score():
    getSentiment.runSentiment()
    with open("result/scores.json") as f:
        scoreJSON = json.load(f)
    scoreJSON['OA_sent'] = (-1.0*scoreJSON["Highly_Neg"] + -0.5*scoreJSON["Moderately_Neg"] + 0.5*scoreJSON["Moderately_Pos"] +\
			1.0*scoreJSON["Highly_Pos"]) / (scoreJSON["Highly_Pos"] + scoreJSON["Moderately_Pos"] + \
			scoreJSON["Neutral"] + scoreJSON["Moderately_Neg"] + scoreJSON["Highly_Neg"])
    print(scoreJSON)    
    return render_template("sentimentGoogleChart.html",  sentJson = scoreJSON)

@app.route("/runButton.php")
def refresh_score():
    getSentiment.runSentiment()
    with open("result/scores.json") as f:
        scoreJSON = json.load(f)
    print(scoreJSON)
    return render_template("sentimentGoogleChart.html",  sentJson = scoreJSON)

@app.route("/<path:filename>")
def sendFileRoot(filename):
	return send_from_directory("templates/", filename)

@app.route("/icons/<path:filename>")
def sendFileIcon(filename):
	return send_from_directory("templates/icons/", filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
