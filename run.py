#!/usr/bin/python
import os
import json
import getSentiment
from flask import Flask, render_template, send_from_directory
app = Flask(__name__)

@app.route("/scores")
def template_score():
    getSentiment.write_score()
    with open("result/scores.json") as f:
        scoreJSON = json.load(f)
    print(scoreJSON)
    return render_template("sentimentGoogleChart.html", 
        Highly_Neg = scoreJSON["Highly_Neg"], Moderately_Neg = scoreJSON["Moderately_Neg"], \
        Neutral = scoreJSON["Neutral"], \
        Moderately_Pos = scoreJSON["Moderately_Pos"], Highly_Pos = scoreJSON["Highly_Pos"])

@app.route("/runButton.php")
def refresh_score():
    getSentiment.runSentiment()
    with open("result/scores.json") as f:
        scoreJSON = json.load(f)
    print(scoreJSON)
    return render_template("sentimentGoogleChart.html",
        Highly_Neg = scoreJSON["Highly_Neg"], Moderately_Neg = scoreJSON["Moderately_Neg"], \
        Neutral = scoreJSON["Neutral"], \
        Moderately_Pos = scoreJSON["Moderately_Pos"], Highly_Pos = scoreJSON["Highly_Pos"])

@app.route("/<path:filename>")
def sendFileRoot(filename):
	return send_from_directory("templates/", filename)

@app.route("/icons/<path:filename>")
def sendFileIcon(filename):
	return send_from_directory("templates/icons/", filename)


if __name__ == "__main__":
    print(os.getcwd())
    app.run(host='0.0.0.0', debug=True)
