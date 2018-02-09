#Contains all the routes or pages or views
from flask import Flask,url_for,request,render_template
from app import app
import redis
# Connect to redis datastore
r = redis.StrictRedis(host='localhost',port=6379,db=0,charset='utf-8',decode_responses=True)
#server
@app.route('/')
def hello():
    return render_template('try.html')
