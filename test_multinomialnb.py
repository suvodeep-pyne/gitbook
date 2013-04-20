'''
Created on Apr 20, 2013

@author: Suvodeep Pyne
'''

print 'Test code for Multinomial Naive Bayes'

categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']

from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

#print twenty_train.target_names
#print len(twenty_train.data)

#print "\n".join(twenty_train.data[0].split("\n"))
#print twenty_train.target_names[twenty_train.target[0]]

data = ['the cat', 'the fog']
target = ['animal', 'weather']

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
#X_train_counts = count_vect.fit_transform(twenty_train.data)
X_train_counts = count_vect.fit_transform(data)

#print X_train_counts

#print count_vect.vocabulary_.get(u'algorithm')

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print X_train_tfidf.shape

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, target)

docs_new = ['God is love', 'OpenGL on the GPU is fast']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
predicted_prob = clf.predict_proba(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print '%r => %s' % (doc, twenty_train.target_names[category])
    
print twenty_train.target_names
for doc, prob in zip(docs_new, predicted_prob):
    print '%r => %s' % (doc, prob)
    
