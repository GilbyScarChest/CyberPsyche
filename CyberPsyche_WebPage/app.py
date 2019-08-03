from flask import Flask, render_template, jsonify
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





app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template("index.html")

@app.route('/data')
def data():
    return render_template("data.html")

@app.route('/model', methods=['GET', 'POST'])
def Scrape_and_Run():

    # message = [1, 0, 1, 0, 0, 0, 1]
    # return jsonify(message)

    #### SCRAPING COMMENTS ####
    filepath = os.path.join("templates", "index.html")
    with open(filepath) as file:
        html = file.read()

    #print(html)

    # Create a Beautiful Soup object
    soup = bs(html, 'html.parser')

    soup.body.find_all("div", class_="comment")

    # Print only the comments
    comments = []
    for item in soup.body.find_all("div", class_="comment"):
        comments.append(item.p.text)

    

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


    tweets_list = [i for i in comments]

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