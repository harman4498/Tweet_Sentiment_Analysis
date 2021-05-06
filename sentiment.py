from flask import Flask,render_template,request,redirect,url_for
import tweepy
import textblob
import pandas as pd
import numpy as np

app= Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def data():
    consumer_key= "*********"
    consumer_secret= "**********"
    access_token= "**********"
    access_token_secret= "**********"

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api= tweepy.API(auth)
    
    if request.method == "POST":
        
        topic= request.form.get("username")
        number_of_tweets= int(request.form.get("number"))
        public_tweets = api.search(topic,count=number_of_tweets)
       
        sentimentDict = {
                'Positive' : [],
                'Negative' : [],
                'Neutral'  : []
                }
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        for tweet in public_tweets:
            analysis = textblob.TextBlob(tweet.text)
            if(analysis.sentiment.polarity > 0.0):
                sentimentDict['Positive'].append(tweet.text)
                positive_count +=1
            elif (analysis.sentiment.polarity < 0.0):
                sentimentDict['Negative'].append(tweet.text)
                negative_count +=1
            elif (analysis.sentiment.polarity == 0.0):
                sentimentDict['Neutral'].append(tweet.text)
                neutral_count +=1
    
        df= pd.DataFrame({key:pd.Series(value) for key, value in sentimentDict.items()})
        return(df.to_html())
        
     
    return render_template("ment.html")
     


app.run(host='localhost', port=6060)