# CyberPsyche

CyberPsyche is a prototype for an app (or widget) which social media websites could use to batch detect, flag and potentially remove or hide inappropriate or agressive comments. Online bullying is a serious problem, the effects of which can range from depression to even suicide, and our children and teens are the most at risk. Even many adult users of social media are often reluctant to log on because of the hate and negativity which currently dominates the online landscape.

## How CyberPsyche Can Help

Using Natural Language Processing (NLP), we can build a machine learning model to analyze social media comments and detect cyber bullying. After that, the user has the ability to remove (or possibly hide) the inappropriate comments.

## What Is NLP?

Natural Language Processing (NLP): a subfield in machine learning concerned with understanding, analyzing, manipulating, and even potentially generating human language.

## How It Works

In our machine learning model, we used NLP n-grams (a set of co-occuring words within a given window) to analyze groupings of particular words to determine the overall sentiment of the comment. Each word is assigned a weight which then, when grouped with other words is assigned a total score and a probability of the context being either appropriate or inappropriate. If the model finds the sentiment of a comment to be inappropriate, the app flags the comment, turning it's background color red, to later be removed or hidden.

The model was initially trained on a dataset of 20,000 random comments from Twitter, which was later combined with 100 additional comments of a political nature. If ever the model mistakenly labels a comment, a feature was designed so that the user can click the specific comment to change it's sentiment rating. That comment and new rating then gets recycled back into the model, which is then retrained, making the algorythm stronger and even more accurate everytime you use it.

## Built Using

* Python
* SciKit Learn
* Pandas
* Flask
* HTML/CSS
* JavaScript
* WTForms

## Acknowledgments

UCI Data Analytics Bootcamp,
Siavash Mortezavi

