'''
Created on Apr 20, 2013

@author: Suvodeep Pyne
'''
from nb_data_collector import NaiveBayesDataCollector

def NaiveBayesClassifier():
    
    def __init__(self, keywords_path, dataset_path):
        self.data_collector = NaiveBayesDataCollector(keywords_path, dataset_path)
        self.keywords = self.data_collector.keywords
        self.dataset = self.data_collector.dataset
