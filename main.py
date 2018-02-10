from flask import Flask
from pandas import pandas
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

from views import *

if __name__ == '__main__':
  app.run()
