# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:45:47 2017

@author: Rachit & Nitesh
"""

from flask import render_template,url_for, flash, redirect, request
from flask import Markup
from main import app
from sentimentCalculator import tweetsSenti
from progress.spinner import Spinner
# from markupsafe import Markup
# index view function suppressed for brevity

@app.route('/', methods=['GET','POST'])
def hello():
    if request.method=='GET':
        return render_template('hello.html')
    elif request.method=='POST':
        twitterHandle = request.form['twitterhandle']
        obj=tweetsSenti()
        world_map_string, world_map_ids,us_map_string, us_map_ids, country_tweets_count, world_country_df = obj.searchTweets(twitterHandle)
            

        return render_template('hello.html', worldPlot = world_map_string,
                              world_map_ids = world_map_ids, usaMapPlot = us_map_string, usa_map_ids = us_map_ids, 
                              country_tweets_count = country_tweets_count, world_country_df = world_country_df)
