from flask import Flask
import os, praw, operator
from flask import render_template
from flask import request


app = Flask(__name__)
reddit = praw.Reddit(client_id=os.environ['client_id'], client_secret=os.environ['client_secret'], password=os.environ["password"], user_agent="biggestContributor", username="papertow3ls")

@app.route('/')
def helloWorld():
    dict = {}
    score_dict = {}
    for submission in reddit.subreddit('BlackPeopleTwitter').hot(limit=1000000000):
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
        print list
        final_list.append(list)
    return render_template('index.html', sub='BlackPeopleTwitter', results=final_list[0:10])

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
        print list
        final_list.append(list)

    return render_template('index.html', sub=sub_name, results=sorted_dict[0:10])
