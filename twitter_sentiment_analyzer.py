#!/usr/bin/env python2

import re
import numpy as np
import matplotlib.pyplot as plt
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):

    def __init__(self):
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment_TextBlob(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        sentiment = ''

        if analysis.sentiment.polarity > 0:
            sentiment = 'positive'
        elif analysis.sentiment.polarity == 0:
            sentiment = 'neutral'
        else:
            sentiment = 'negative'

        return (sentiment, analysis.sentiment.polarity)

    def get_tweets_by_query(self, query, count = 10):
        tweets = []
        sentiment = []
        sentiment_scores = []

        try:
            fetched_tweets = self.api.search(q = query, count = count, tweet_mode='extended')

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment_TextBlob(tweet.full_text)
                sentiment.append(parsed_tweet['sentiment'][0])
                sentiment_scores.append(parsed_tweet['sentiment'][1])

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return (tweets, sentiment, sentiment_scores)

        except tweepy.TweepError as e:
            print("Error : " + str(e))

    def get_tweets_by_home(self, count = 10):
        tweets = []
        sentiment = []
        sentiment_scores = []

        try:
            fetched_tweets = tweepy.Cursor(self.api.home_timeline, tweet_mode='extended').items(count)

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment_TextBlob(tweet.full_text)
                sentiment.append(parsed_tweet['sentiment'][0])
                sentiment_scores.append(parsed_tweet['sentiment'][1])

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return (tweets, sentiment, sentiment_scores)

        except tweepy.TweepError as e:
            print("Error : " + str(e))

    def get_tweets_by_user(self, name, count = 10):
        tweets = []
        sentiment = []
        sentiment_scores = []

        try:
            fetched_tweets = self.api.user_timeline(screen_name=name, count=count, tweet_mode='extended')

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment_TextBlob(tweet.full_text)
                sentiment.append(parsed_tweet['sentiment'][0])
                sentiment_scores.append(parsed_tweet['sentiment'][1])

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return (tweets, sentiment, sentiment_scores)

        except tweepy.TweepError as e:
            print("Error : " + str(e))

def main():
    api = TwitterClient()
    query = 'Twitter'
    #tweets, sentiment, sentiment_scores = api.get_tweets_by_home(count = 20)
    tweets, sentiment, sentiment_scores = api.get_tweets_by_query(query = query, count = 200)
    #tweets, sentiment, sentiment_scores = api.get_tweets_by_user(name = 'realDonaldTrump', count = 200)

    ptweets = [tweet for tweet in tweets if tweet['sentiment'][0] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'][0] == 'negative']

    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    print("Neutral tweets percentage: {} %".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))

    ptweets = sorted(ptweets, reverse=True)
    ntweets = sorted(ntweets)

    print("\nPositive tweets:")
    for tweet in ptweets[:5]:
        print(tweet['text'])
        print

    print("\nNegative tweets:")
    for tweet in ntweets[:5]:
        print(tweet['text'])
        print

    labels = 'Positive', 'Negative', 'Neutral'
    sizes = [len(ptweets), len(ntweets), len(tweets) - len(ptweets) - len(ntweets)]
    colors = ['green', 'red', 'deepskyblue']
    explode = (0.05, 0.05, 0.05)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=140)
    plt.axis('equal')
    plt.title('Query = "%s"' %query)
    plt.show()

    plt.hist(sentiment_scores, bins=[-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], edgecolor='black', linewidth=0.75)
    plt.xlabel("Score bin")
    plt.ylabel("Number of tweets")
    plt.show()

    plt.hist(sentiment, bins=3, edgecolor='black', linewidth=0.75)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of tweets")
    plt.show()

if __name__ == "__main__":
    main()

