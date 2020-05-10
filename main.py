from flask import Flask, redirect, render_template, request # one-liner import for flask
import os, praw, operator


app = Flask(__name__)

siteName = "http://127.0.0.1:5000" # change this to an environment var, Someday^TM

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['client_secret'], password=os.environ["reddit_password"], user_agent="biggestContributor", username="papertow3ls")


@app.route('/')
def index():
    dict = {}
    score_dict = {}
    for submission in reddit.subreddit('Purdue').hot(limit=1000000000):
        if(submission.author == None):
            continue
        author = submission.author.name
        if(author not in dict):
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
        final_list.append(list)
    return render_template('index.html', sub='Purdue', results=final_list)



@app.route('/search', methods=['GET', 'POST'])
def search_route():
    return render_template('search.html')


@app.route('/results', methods=['GET', 'POST'])
def results_route():

    ret_dict = {}
    score_dict = {}
    sub_name = request.args.get('sub', '')
    limit_num = request.args.get('num', '')
    sub = reddit.subreddit(request.args.get('sub', ''))
    for submission in sub.new(limit=int(limit_num)):
        if(submission.author == None):
            continue
        author = submission.author.name
        if(author not in ret_dict):
            ret_dict[author] = 1
        else:
            count = ret_dict[author]
            count += 1
            ret_dict[author] = count
        if(author not in score_dict):
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
