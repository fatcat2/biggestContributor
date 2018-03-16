#!/usr/bin/env python

# "python" defaults to a 2.7 shell on Linux, check it's the same for MacOSX

from flask import Flask, redirect, render_template, request
import os, praw, operator


app = Flask(__name__)

siteName = "http://127.0.0.1:5000" # change this to an environment var, someday^TM

reddit = praw.Reddit(client_id=os.environ['client_id'], client_secret=os.environ['client_secret'], password=os.environ["password"], user_agent="biggestContributor", username="papertow3ls")

@app.route('/')
def helloWorld(): # must immediately return something, can not have any other code or it throws an error in flask on Linux.

    return redirect("{}/search".format(siteName))
    # dict = {}
    # score_dict = {}
    # for submission in reddit.subreddit('BlackPeopleTwitter').hot(limit=1000000000):
    #     if(submission.author == None):
    #         continue
    #     author = submission.author.name
    #     if(not dict.has_key(author)):
    #         dict[author] = 1
    #     else:
    #         count = dict[author]
    #         count += 1
    #         dict[author] = count
    #     if(not score_dict.has_key(author)):
    #         score_dict[author] = submission.score
    #     else:
    #         count = score_dict[author]
    #         count += submission.score
    #         score_dict[author] = count
    #
    # sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    # sorted_dict.reverse()
    # final_list = [];
    # for list in sorted_dict:
    #     list = list + (score_dict[list[0]],)
    #     #print list
    #     final_list.append(list)
    # return render_template('index.html', sub='BlackPeopleTwitter', results=final_list[0:10])


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
    final_list = [];
    for list in sorted_dict:
        list = list + (score_dict[list[0]],)
        final_list.append(list)

    return render_template('index.html', sub=sub_name, results=final_list[0:10])
