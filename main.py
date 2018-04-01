#!/usr/bin/env python2

# "python" defaults to a 2.7 shell on Linux, check it's the same for MacOSX

from flask import Flask, redirect, render_template, request # one-liner import for flask
import os, praw, operator


app = Flask(__name__)

siteName = "http://127.0.0.1:5000" # change this to an environment var, Someday^TM

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['client_secret'], password=os.environ["reddit_password"], user_agent="biggestContributor", username="papertow3ls")


@app.route('/')
def helloWorld():
    dict = {}
    score_dict = {}
    for submission in reddit.subreddit('BlackPeopleTwitter').hot(limit=1000000000):
        if(submission.author == None):
            continue
        author = submission.author.name
        if(not author in dict):
            dict[author] = 1
        else:
            count = dict[author]
            count += 1
            dict[author] = count
        if(not author in score_dict):
            score_dict[author] = submission.score
        else:
            count = score_dict[author]
            count += submission.score
            score_dict[author] = count

    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    sorted_dict.reverse()
    final_list = []
    for list in sorted_dict:
        list = list + (score_dict[list[0]],)
        #print list
        final_list.append(list)
    return render_template('index.html', sub='BlackPeopleTwitter', results=final_list)



@app.route('/search', methods=['GET', 'POST'])
def hello():
    return render_template('search.html')


@app.route('/results', methods=['GET', 'POST'])
def showResults():

    dict = {}
    score_dict = {}
    sub_name = request.args.get('sub', '')
    limit_num = request.args.get('num', '')
    sub = reddit.subreddit(request.args.get('sub', ''))
    for submission in sub.new(limit=int(limit_num)):
        if(submission.author == None):
            continue
        author = submission.author.name
        if(not dict.has_key(author)):
            dict[author] = 1
        else:
            count = dict[author]
            count += 1
            dict[author] = count
        if(not score_dict.has_key(author)):
            score_dict[author] = submission.score
        else:
            count = score_dict[author]
            count += submission.score
            score_dict[author] = count
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    sorted_dict.reverse()
    final_list = []
    for list in sorted_dict:
        list = list + (score_dict[list[0]],)
        final_list.append(list)

    return render_template('index.html', sub=sub_name, results=final_list)
