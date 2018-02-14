# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:45:47 2017

@author: Rachit & Nitesh
"""

from flask import render_template,url_for, flash, redirect, request
from flask import Markup
from main import app
from sentimentCalculator import tweetsSenti
# from markupsafe import Markup
# index view function suppressed for brevity

@app.route('/', methods=['GET','POST'])
def hello():
    if request.method=='GET':
        return render_template('hello.html')
    elif request.method=='POST':
        twitterHandle = request.form['twitterhandle']
        obj=tweetsSenti()
        world_map_string = obj.searchTweets(twitterHandle)
        print("Yay")
        return render_template('hello.html')
