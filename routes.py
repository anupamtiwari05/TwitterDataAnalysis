#Contains all the routes or pages or views
from flask import Flask,url_for,request,render_template
from main import app

#server
@app.route('/')
def hello():
    return render_template('hello.html')
