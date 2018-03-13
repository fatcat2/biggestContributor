from flask import Flask
import os
from flask import render_template

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return render_template('index.html')
