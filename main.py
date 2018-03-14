from flask import Flask
import os, praw, operator
from flask import render_template

app = Flask(__name__)

@app.route('/')
def helloWorld():
    reddit = praw.Reddit(client_id=os.environ['client_id'], client_secret=os.environ['client_secret'], password=os.environ["password"], user_agent="biggestContributor", username="papertow3ls")
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

@app.route('/search', methods=['GET', 'POST')
