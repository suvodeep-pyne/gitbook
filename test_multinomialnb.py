'''
Created on Apr 20, 2013
@author: Suvodeep Pyne
'''
import re

def tokenize(text):
    return [tok.strip().lower() for tok in re.compile(r",\s*").split(text)]

print 'Test code for Multinomial Naive Bayes'

categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']

from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

#print twenty_train.target_names
#print len(twenty_train.data)

#print "\n".join(twenty_train.data[0].split("\n"))
#print twenty_train.target_names[twenty_train.target[0]]



data = ['the, cat, cat, cat, cat, dog, mammal', 'the, fog, fog, fog, fog']
target = ['animal', 'weather']

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer(min_df=1)
#X_train_counts = count_vect.fit_transform(twenty_train.data)
X_train_counts = count_vect.fit_transform(data)

print 'Headers:', count_vect.get_feature_names()
print 'X_train_counts:\n', X_train_counts.toarray()
print count_vect.vocabulary_.get(u'algorithm')
print 'count_vect.vocabulary_:', count_vect.vocabulary_

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print 'X_train_tfidf.shape:', X_train_tfidf.shape

from sklearn.naive_bayes import MultinomialNB
#clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
clf = MultinomialNB().fit(X_train_tfidf, target)

docs_new = ['fog', 'cat']
X_new_counts = count_vect.transform(docs_new)
print 'X_new_counts:', X_new_counts
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
predicted_prob = clf.predict_proba(X_new_tfidf)

print 'Prediction:'
for doc, category in zip(docs_new, predicted):
#    print '%r => %s' % (doc, twenty_train.target_names[category])
    print '%r => %s' % (doc, category)

print twenty_train.target_names
for doc, prob in zip(docs_new, predicted_prob):
    print '%r => %s' % (doc, prob)
    
