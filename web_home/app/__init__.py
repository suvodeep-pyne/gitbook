'''
Created on Apr 29, 2013

@author: Suvodeep Pyne
'''

from flask import Flask

application = Flask(__name__)
application.config.from_object('config')

from app import routes
