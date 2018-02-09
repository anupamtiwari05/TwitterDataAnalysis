from flask import Flask
app = Flask(__name__)
import pandas as pd


from views import *

if __name__ == '__main__':
  app.run()
