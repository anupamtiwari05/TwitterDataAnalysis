# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:45:47 2017

@author: Rachit & Nitesh
"""

class tweetsSenti:
    
        
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    def searchTweets(self, q):
        from twitter import Twitter,  OAuth, TwitterHTTPError
        import pandas as pd
        from pandas.io.json import json_normalize
        
        return q + 'Nitesh'
