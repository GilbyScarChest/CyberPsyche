#################################################
# Dependencies
#################################################
from flask import Flask, render_template, jsonify, request, make_response
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
# This route is the Home Page
@app.route('/', methods=['GET', 'POST'])
def hello():

    #### Getting comments posted from form to put in json file ####
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
#### MAKE THE MODEL SMARTER ####
@app.route('/admin', methods=['POST'])
def admin():
    
    comment_to_add = request.form['Comment']
    rating_to_add = request.form['Rating']

    my_dict = {"Comment": comment_to_add, "Rating": rating_to_add}

    resp = make_response(json.dumps(my_dict))
    resp.status_code = 200

    print(comment_to_add) # This is the variable for "Comment" to add to DataFrame
    print(rating_to_add)  # This is the variable for "Rating" to add to DataFrame

    return resp


# This route is where the model runs
@app.route('/model', methods=['GET', 'POST'])
def Scrape_and_Run():

    # Adding the comments which are hard-coded on the site
    comments_temp = ['What A Beautiful Day!!!', 'Fuck you and the horse you rode in on!', 'Fuck EVERYTHING!!! YOU ASSHOLE']

    # Loading newly posted comments from json
    with open('static/comments.json', 'r') as file:
        comments_dict = json.load(file)

    # Add newly posted comments from json to list of hard-coded comments
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

    X_all =  list(new_df.content)
    y = list(new_df.rating)

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