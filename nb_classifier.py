'''
Created on Apr 20, 2013

@author: Suvodeep Pyne
Edited: Garima Agarwal
'''

import re
import pprint as pp

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from nb_data_collector import NaiveBayesDataCollector
from nb_data_collector import tokenizer_regex

def tokenize(text):
    return re.findall(tokenizer_regex, text)

class NaiveBayesClassifier():
    tfidf_transformer = TfidfTransformer(norm = None)
    
    def __init__(self, keywords_path, dataset_path):
        print 'Initializing NaiveBayesClassifier..'
        self.data_collector = NaiveBayesDataCollector(keywords_path, dataset_path)
        
        self.keywords = self.data_collector.keywords
        self.documents = self.data_collector.documents
        self.target_classes = self.data_collector.target_classes
        
        self.count_vectorizer = CountVectorizer(min_df=1, tokenizer=tokenize, vocabulary = self.keywords)
    
    def train(self):
        print 'Training Naive Bayes..'
        
        print 'Running Count Vectorizer..'
        X_train_counts = self.count_vectorizer.fit_transform(self.documents)
        
#        print 'Headers:', self.count_vectorizer.get_feature_names()
#        print 'X_train_counts:\n', X_train_counts.toarray()
#        print 'count_vect.vocabulary_:', self.count_vectorizer.vocabulary_
        
        print 'Performing tf-idf transform..'
        
        X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)
        #print 'X_train_tfidf.shape:', X_train_tfidf.shape
#        print 'X_train_tfidf:\n', X_train_tfidf.toarray()
        
        self.clf = MultinomialNB(fit_prior=False).fit(X_train_tfidf, self.target_classes)
        
    def classify(self, param):
        if isinstance(param, list):
            docs_new = param
        else:
            docs_new = [param]
        X_new_counts = self.count_vectorizer.transform(docs_new)
#        print 'X_new_counts:', X_new_counts
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)
        
        predicted = self.clf.predict(X_new_tfidf)
        predicted_prob = self.clf.predict_proba(X_new_tfidf)
        
        """
        print
        print 'Prediction:'
        for doc, category in zip(docs_new, predicted):
            print '%r => %s' % (doc, category)
        
        print
        for doc, prob in zip(docs_new, predicted_prob):
            print '%r => %s' % (doc, prob)
        """
        return_val = []
        for row in predicted_prob:
            prob_data = {}
            for prob, category in zip(row, self.clf.classes_):
               prob_data[category] = prob
            return_val.append(prob_data)
        return return_val
            
if __name__ == "__main__":        
    from resource_manager import ResourceManager
    rm = ResourceManager()
    nb = NaiveBayesClassifier(rm.TRAINDATA_VOCAB, rm.TRAINDATA_DATASET)
    nb.train()
    docs_new = ['regression']
    #docs_new = ['asdfasdfasdf', 'jquery', 'data mining', 'regression', 'search', 'vector space', 'Knowledge Discovery', 'Kernel']
    result = nb.classify(docs_new)
    
    pp.pprint(result)
    
    print
    print 'Target classes:', nb.target_classes
