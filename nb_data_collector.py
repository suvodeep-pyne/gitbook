'''
Created on Apr 20, 2013

@author: Suvodeep Pyne
'''
import re

url = 'http://en.wikipedia.org/wiki/Machine_learning'

CATEGORIES = [ 'Machine Learning', 'Artificial Intelligence']

class NaiveBayesDataCollector():
    keywords = set()
    
    def __init__(self, keywords_path, dataset_path):
        self.keywords_path = keywords_path
        self.dataset_path = dataset_path
        
        self.process_keywords()
    
    def read(self, filepath):
        content = open(filepath, 'r').read()
        words = re.findall("[a-zA-Z0-9]{3,}", content.lower())
        return words
        
    def process_keywords(self):
        for word in self.read(self.keywords_path):
            self.keywords.add(word)
                
nb = NaiveBayesDataCollector('train_data\\allterms\\allTerms.txt', '')
print nb.keywords

    
