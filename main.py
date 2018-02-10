from flask import Flask
app = Flask(__name__)

WSGIApplicationGroup %{GLOBAL}
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

from views import *

if __name__ == '__main__':
  app.run()
