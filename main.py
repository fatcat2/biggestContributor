from typing import Any, Dict, List

from flask import Flask, redirect, render_template, request
import os, praw, operator

from utils import get_subreddit_results, SubNotFoundException

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['CLIENT_SECRET'], user_agent="biggestContributor")


@app.route('/')
def default_route():
    subreddit_results = get_subreddit_results("Purdue", 100, reddit)

    return render_template("index.html", sub='Purdue', results=subreddit_results, limit=int(100))


@app.route('/search', methods=['GET', 'POST'])
def search_route():
    return render_template('search.html')


@app.route('/results', methods=['GET', 'POST'])
def results_route():
    sub_name = request.args.get('sub', '')

    if "r/" == sub_name[:2]:
        sub_name = sub_name[2:]

    limit_num = request.args.get('num', '') or 100

    try:
        subreddit_results = get_subreddit_results(sub_name, int(limit_num), reddit)
    except SubNotFoundException:
        return render_template("error.html", sub=sub_name)

    return render_template('index.html', sub=sub_name, results=subreddit_results, limit=int(limit_num))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
