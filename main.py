from typing import Any, Dict, List

from flask import Flask, redirect, render_template, request # one-liner import for flask
import os, praw, operator

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['CLIENT_SECRET'], user_agent="biggestContributor")


@app.route('/')
def index():
    subreddit_results = get_subreddit_results("Purdue", 100)

    return render_template("index.html", sub='Purdue', results=subreddit_results)


@app.route('/search', methods=['GET', 'POST'])
def search_route():
    return render_template('search.html')


def get_subreddit_results(subreddit_name: str, limit_num: int) -> List[Dict[Any, Any]]:
    """Gets highest contributing redditors to a specific subreddit.

    Args:
            subreddit_name (str): the name of the desired subreddit.
            limit_num (int): the number of posts to look at
            reddit (praw.Reddit): a praw instance to use
    """
    ret_dict = {}
    score_dict = {}
    sub = reddit.subreddit(subreddit_name)

    for submission in sub.new(limit=int(limit_num)):
        if(submission.author == None):
            continue
        author = submission.author.name
        if(author not in ret_dict):
            ret_dict[author] = 1
        else:
            ret_dict[author] += 1
        if(author not in score_dict):
            score_dict[author] = submission.score
        else:
            score_dict[author] += submission.score
    sorted_dict = sorted(ret_dict.items(), key=operator.itemgetter(1))
    sorted_dict.reverse()
    final_list = []
    for list in sorted_dict:
        list = list + (score_dict[list[0]],)
        final_list.append(list)

    return final_list


@app.route('/results', methods=['GET', 'POST'])
def results_route():
    sub_name = request.args.get('sub', '')
    limit_num = request.args.get('num', '')

    subreddit_results = get_subreddit_results(sub_name, int(limit_num))

    return render_template('index.html', sub=sub_name, results=subreddit_results)

if __name__ == "__main__":
    app.run(debug=True)
