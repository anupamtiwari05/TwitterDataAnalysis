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
        return render_template('hello.html',likesCount=count, likeButtonColor='cornflowerblue',likeButtonValue='Like')
    elif request.method=='POST':
        twitterHandle = request.form['twitterhandle']
        likeButtonValue = request.form['hiddenButtonValue']
        hiddenQueryText = request.form['hiddenQueryValue']
        
        if likeButtonValue == 'Like':
            likeButtonColor='cornflowerblue'
        elif likeButtonValue == 'UnLike':
            likeButtonColor='mediumseagreen'

      
        path=os.getcwd()
        fullPath=os.path.join(path,'Databases\\LikesCount.txt')
        countFileR=open(fullPath,'r')
        count = countFileR.read()
        countFileR.close()
        

        if hiddenQueryText == '':
            newCount=0
            likeButtonColor=''
            if likeButtonValue=="UnLike":
                newCount= int(count) + 1
                likeButtonColor='mediumseagreen'
                likeButtonValue='UnLike'
            elif likeButtonValue=="Like":
                newCount= int(count) - 1
                likeButtonColor='cornflowerblue'
                likeButtonValue='Like'
             
        countFileW = open(fullPath,'w')
        if newCount == 0:
            countFileW.write(count)
        elif newcount != 0:
            countFileW.write(str(newCount))
        
        countFileW.close()

        if twitterHandle!='' and hiddenQueryText!='':
           obj=tweetsSenti()
           world_map_string, world_map_ids, us_map_string, us_map_ids, world_tweets_count, world_country_df,country_tweets_count, summary_df_Country, bar_string, bar_ids = obj.searchTweets(twitterHandle)
           if(world_map_string==""):
              return render_template('hello.html', worldPlot = world_map_string, world_map_ids = world_map_ids, usaMapPlot = us_map_string, usa_map_ids = us_map_ids, 
                              world_tweets_count = world_tweets_count, world_country_df = world_country_df,country_tweets_count=country_tweets_count, summary_df_Country = summary_df_Country,
                              bar_string = bar_string, bar_ids = bar_ids, exception = "Raise Exception", likesCount = newCount,likeButtonColor = likeButtonColor,likeButtonValue = likeButtonValue)
           else:
              return render_template('hello.html', worldPlot = world_map_string, world_map_ids = world_map_ids,
                                  usaMapPlot = us_map_string, usa_map_ids = us_map_ids, world_tweets_count = world_tweets_count, world_country_df = world_country_df,
                                  country_tweets_count=country_tweets_count, summary_df_Country = summary_df_Country,
                                  barPlot = bar_string, bar_ids = bar_ids, likesCount = newCount,likeButtonColor = likeButtonColor,likeButtonValue = likeButtonValue)
        elif(likeButtonValue!=""):
            return render_template('hello.html', likesCount = newCount,likeButtonColor = likeButtonColor,likeButtonValue = likeButtonValue)
        else:
            return render_template('hello.html', likesCount = newCount,likeButtonColor = likeButtonColor,likeButtonValue = likeButtonValue)
