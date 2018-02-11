# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:45:47 2017

@author: Rachit & Nitesh
"""

class tweetsSenti:

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    def searchTweets(self, q):
        import numpy as np
        import pandas as pd
        import re
        from twitter import Twitter, OAuth, TwitterHTTPError
        from pandas.io.json import json_normalize
        
        ACCESS_TOKEN = '136600388-9iihe7SFq8nZUOL5GjxoZlPbxW2MYcScWlZ6sD3a'
        ACCESS_SECRET = 'ScmAR4iYHCxuPHhYMifirTK0h2Jhdqt1p10uoz9lHTshT'
        consumer_key = 'bto0MsRvjjfkrl4QpndjaUneg'
        consumer_secret = '5zr7Xr9y4AbKgUCuWRmQGaMvizwg48HpVeyjbSZC4j350rIYPF'
    
        oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, consumer_key, consumer_secret)
        twitterObj = Twitter(auth=oauth)
        #q = 'modi'
        count = 100
        try:
            search_results = twitterObj.search.tweets(q=q,count = count)
        except TwitterHTTPError:
            return 'twitter server error'
        Original_status_df = json_normalize(search_results,['statuses'])
        Original_status_df = pd.DataFrame(Original_status_df)
        min_id = min(Original_status_df['id'])
        max_id = max(Original_status_df['id'])

        while len(Original_status_df) < 300:
            try:
                search_results = twitterObj.search.tweets(q=q,count=count,max_id = min_id)
                results = json_normalize(search_results,['statuses'])
                Original_status_df = Original_status_df.append(results)
                min_id = min(results['id'])
                max_id = max(results['id'])
            except TwitterHTTPError:
                return 'twitter server error'

        Original_status_df = Original_status_df.reset_index()
        cleaned_tweets_df = clean_Tweets(Original_status_df)

        return 'Success'

def clean_Tweets(Original_status_df):
    import re
    status_row = []
    location=[]
    tweet_df = Original_status_df[['user','text']]
    for i in range(len(tweet_df)):
        status_ = tweet_df.iloc[i,:]['text'].lower()
        status_ = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',status_)
        status_ = re.sub('@[^\s]+','',status_)
        status_ = re.sub('[^A-Za-z0-9 ]+', '', status_)
        status_ = status_.replace('rt','')
        status_row.append(status_)
        
        try:
            location_ = tweet_df.iloc[i,:]['user']['location']
            location.append(location_)
        except IndexError:
            location.append("")

    tweet_df['text'] = status_row
    tweet_df['Location_User'] = location
   
    return tweet_df

        
