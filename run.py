#!/usr/bin/python
import os
import json
import getSentiment
from flask import Flask, render_template
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

if __name__ == "__main__":
    print(os.getcwd())
    app.run(host='0.0.0.0', debug=True)
