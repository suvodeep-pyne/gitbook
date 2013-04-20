'''
Created on Apr 20, 2013

@author: Suvodeep Pyne
'''


import requests

url = 'http://en.wikipedia.org/wiki/Machine_learning'

CATEGORIES = [ 'Machine Learning', 'Artificial Intelligence']

class NaiveBayesDataCollector():
    
    def __init__(self):
        pass
    
    def read(self, url):
        