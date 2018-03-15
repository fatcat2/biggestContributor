from flask import Flask
import os, praw, operator
from flask import render_template
from flask import request


app = Flask(__name__)
reddit = praw.Reddit(client_id=os.environ['client_id'], client_secret=os.environ['client_secret'], password=os.environ["password"], user_agent="biggestContributor", username="papertow3ls")

@app.route('/')
def helloWorld():
    dict = {}
    for submission in reddit.subreddit('BlackPeopleTwitter').hot(limit=1000000000):
        author = submission.author.name
        if(not dict.has_key(author)):
            dict[author] = 1
        else:
            count = dict[author]
            count += 1
            dict[author] = count
    
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    sorted_dict.reverse()

    stop_count = 0

    return render_template('index.html', results=sorted_dict[0:10])

@app.route('/search', methods=['GET', 'POST'])
def hello():
    return render_template('search.html')

@app.route('/results', methods=['GET', 'POST'])
def showResults():
    dict = {}
    sub_name = request.args.get('sub', '')
    sub = reddit.subreddit(request.args.get('sub', ''))
    for submission in sub.hot(limit=1000000):
        author = submission.author.name
        if(not dict.has_key(author)):
            dict[author] = 1
        else:
            count = dict[author]
            count += 1
            dict[author] = count
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    sorted_dict.reverse()

    return render_template('index.html', sub=sub_name, results=sorted_dict[0:10])
