# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:45:47 2017

@author: Rachit & Nitesh
"""

from flask import render_template,url_for, flash, redirect, request
from pycountry import countries
from flask import Markup
from main import app
from sentimentCalculator import tweetsSenti
import os

# from markupsafe import Markup
# index view function suppressed for brevity

@app.route('/', methods=['GET','POST'])
def hello():
    if request.method=='GET':
        path=os.getcwd()
        fullPath=os.path.join(path,'Databases\\LikesCount.txt')
        countFileR=open(fullPath,'r')
        count = countFileR.read()
        countFileR.close()
        return render_template('hello.html', likesCount=count, likeButtonColor='cornflowerblue',likeButtonValue='Like')
    elif request.method=='POST':
        twitterHandle = request.form['twitterhandle']
        
        obj=tweetsSenti()

        world_map_string, world_map_ids, us_map_string, us_map_ids, world_tweets_count, world_country_df,country_tweets_count, summary_df_Country = obj.searchTweets(twitterHandle)
        if(world_map_string==""):
            return render_template('hello.html', worldPlot = world_map_string, world_map_ids = world_map_ids, usaMapPlot = us_map_string, usa_map_ids = us_map_ids, 
                              world_tweets_count = world_tweets_count, world_country_df = world_country_df,country_tweets_count=country_tweets_count, summary_df_Country = summary_df_Country,
                              exception = "Raise Exception")
        else:
            return render_template('hello.html', worldPlot = world_map_string, world_map_ids = world_map_ids,
                                  usaMapPlot = us_map_string, usa_map_ids = us_map_ids, 
                                  world_tweets_count = world_tweets_count, world_country_df = world_country_df,
                                 country_tweets_count=country_tweets_count, summary_df_Country = summary_df_Country)
