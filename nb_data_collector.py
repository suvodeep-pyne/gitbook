'''
Created on Apr 20, 2013

@author: Suvodeep Pyne
'''
import re
import os
import pprint as pp

url = 'http://en.wikipedia.org/wiki/Machine_learning'

CATEGORIES = [ 'Machine Learning', 'Artificial Intelligence']
tokenizer_regex = "[a-zA-Z][a-zA-Z_-]+[a-zA-Z]";

class NaiveBayesDataCollector():
    keywords = set()
    
    documents = []
    target_classes = []
    
    def __init__(self, keywords_path, dataset_path):
        self.keywords_path = keywords_path
        self.dataset_path = dataset_path
        
        self.process_keywords()
        self.process_dataset()
    
    def read_file(self, filepath):
        content = open(filepath, 'r').read()
        words = re.findall(tokenizer_regex, content.lower())
        return words
        
    def process_keywords(self):
        print 'Processing Keywords..'
        for root, subfolders, files in os.walk(self.keywords_path):
            for filename in files:
                if filename.endswith(".txt"):
                    self.keywords.update(self.read_file(os.path.join(root, filename)))
        print 'done.'
            
    def process_dataset(self):
        print 'Processing Dataset..'
        fileList = []
        fileSize = 0
    
        for root, subfolders, files in os.walk(self.dataset_path):
            print 'Scanning folder: ', root
            for filename in files:
                if filename.endswith(".txt"):
                    filepath = os.path.join(root, filename)
                    fileSize += os.path.getsize(filepath)
    
                    feature = os.path.basename(root)
                    doc_content = open(filepath, 'r').read().lower()
                    
                    self.target_classes.append(feature)
                    self.documents.append(doc_content)
                    fileList.append(filepath)
    
        print "Total Size is {0} bytes".format(fileSize)
        print 'Total Files: ', len(fileList)
        print 'filelist:', fileList
        
        print 'done.'
        
if __name__ == "__main__":        
    nb = NaiveBayesDataCollector('train_data\\allterms', 'train_data\\dataset')
    
    print
    print 'Keyword List:', nb.keywords
    print 'Target classes:', nb.target_classes
    #for doc in nb.documents:
    #    print doc
