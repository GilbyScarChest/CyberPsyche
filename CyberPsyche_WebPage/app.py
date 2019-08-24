#################################################
# Dependencies
#################################################
from flask import Flask, render_template, jsonify, request
from splinter import Browser
import os
from bs4 import BeautifulSoup as bs
import requests
import time

import pandas as pd
import numpy as np
import json
import re

from nltk.corpus import stopwords
import nltk
from sklearn.externals import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from sklearn.svm import LinearSVC

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import Column, Integer, String, Float

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from datetime import datetime as dt

from config import Config



#################################################
# Database Setup
#################################################
# Create an engine for the data.sqlite database
engine = create_engine("sqlite:///db/data.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# This is where we create our tables in the database
Base.metadata.create_all(engine)

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

#Make new comments.json
with open('static/comments.json', 'w') as file:
    json.dump({}, file)


#################################################
# Class Setup
#################################################
class Comments(Base):
    __tablename__ = 'comments_sqlite'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500)) 
    rating = db.Column(db.Integer)

    def __init__(self, comment, rating):
        self.comment = comment
        self.rating = rating

class CommentForm(FlaskForm):
    comment = TextField('Comment', widget=TextArea(), validators=[DataRequired()], default="")
    # submit = SubmitField('Comment your ass off')

#################################################
# Routes
#################################################
# user_comments = []
# comments = []
# This route is the Home Page
@app.route('/', methods=['GET', 'POST'])
def hello():
    form = CommentForm()
    with open("static/comments.json", 'r') as file:
        comments = json.load(file)
        # Python debugger
        # import pdb; pdb.set_trace()

    if form.validate_on_submit():
        comment = form.comment.data.strip()
        timestamp = dt.now().strftime('%c')
        comments[timestamp] = comment
        with open('static/comments.json', 'w') as outfile:
            json.dump(comments, outfile)

    return render_template("index.html", form=form, comments=comments)

# This route gets you the Training Data
@app.route('/data')
def data():
    return render_template("data.html")

# This route is the db where comments and rating are stored
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
    
    # results = engine.execute('SELECT * FROM comments_sqlite').fetchall()

    # comment = [result['comment'] for result in results]
    # rating = [result['rating'] for result in results]
    
    # value = request.args.get('Comment')
    # #print(value)
    # user_comments.append(value)
    #print(comments)

    # wordlist = json.loads(requests.get('wordlist'))
    # print(wordlist)
    # # do some stuff
    # return jsonify(result=wordlist)


    trace = {
        "Comment": value,
        # "Rating": rating
    }

    return jsonify(trace)


# This route is where the model runs
@app.route('/model', methods=['GET', 'POST'])
def Scrape_and_Run():

    # message = [1, 0, 1, 0, 0, 0, 1]
    # return jsonify(message)
    
    

    #### SCRAPING COMMENTS ####
    # filepath = os.path.join("templates", "index.html")
    # with open(filepath) as file:
    #     html = file.read()


    #### Using Browser #############################
    # executable_path = {"executable_path": "C:\\Users\\tdgso\\Desktop\\chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)

    # url = "http://127.0.0.1:5000/" # Not sure if it'll work but I think it will

    # browser.visit(url)

    # time.sleep(2)

    # html = browser.html
    ##################################################

    # Create a Beautiful Soup object
    # soup = bs(html, 'html.parser')

    # soup.body.find_all("div", class_="comment")

    # # Print only the comments
    # for item in soup.body.find_all("div", class_="comment"):
    #     comments.append(item.p.text)

    # # merged_list = comments + user_comments

    # print(comments)
    comments_temp = ['What A Beautiful Day!!!', 'Fuck you and the horse you rode in on!', 'Fuck EVERYTHING!!! YOU ASSHOLE']
    with open('static/comments.json', 'r') as file:
        comments_dict = json.load(file)

    comments_list = comments_temp + list(comments_dict.values())

    #### Pre Processing ####
    REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    NO_SPACE = ""
    SPACE = " "

    def preprocess_reviews(reviews):
        
        reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
        reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]
        
        return reviews


    df = pd.read_json("Resources/Data_cyb.json", lines = True, orient = "columns")

    rating = []

    for i in df["annotation"]:
        rating.append(int(i["label"][0]))
        
    df["rating"] = rating

    tweets = pd.read_csv("Resources/Test_Twitter_Comments.csv")

    new_df1 = df[["content", "rating"]]

    new_df = pd.concat([new_df1,tweets])

    X_all = [i[1]["content"] for i in new_df.iterrows()]
    y = [i[1]["rating"] for i in new_df.iterrows()]

    reviews_train_clean = preprocess_reviews(X_all)

    #This is where to put the comments list variable
    tweets_list = [i for i in comments_list]

    twitter_cleaned = preprocess_reviews(tweets_list)

    #### FITTING THE MODEL ####
    stop_words = stopwords.words('english')
    ngram_vectorizer = CountVectorizer(binary=True, ngram_range=(1, 3), stop_words=stop_words)
    ngram_vectorizer.fit(reviews_train_clean)

    X = ngram_vectorizer.transform(reviews_train_clean)

    final = LinearSVC(tol=.000001,C=0.06)
    final.fit(X, y)

    tws = ngram_vectorizer.transform(twitter_cleaned)

    predictions = final.predict(tws)

    print(predictions)

    predictions = predictions.tolist()

    return jsonify(predictions)






if __name__ == '__main__':
    app.run()