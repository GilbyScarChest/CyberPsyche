from splinter import Browser
import os
from bs4 import BeautifulSoup as bs
import requests
import time

filepath = os.path.join("CyberPsyche_WebPage", "index.html")
with open(filepath) as file:
    html = file.read()

# Create a Beautiful Soup object
soup = bs(html, 'html.parser')

soup.body.find_all("div", class_="comment")

# Print only the comments
comments = []
for item in soup.body.find_all("div", class_="comment"):
    comments.append(item.p.text)


print(comments)