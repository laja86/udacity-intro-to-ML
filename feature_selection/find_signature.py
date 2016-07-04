#!/usr/bin/python

import pickle
import numpy
numpy.random.seed(42)


### The words (features) and authors (labels), already largely processed.
### These files should have been created from the previous (Lesson 10)
### mini-project.
words_file = "../text_learning/your_word_data.pkl"
authors_file = "../text_learning/your_email_authors.pkl"
word_data = pickle.load( open(words_file, "r"))
authors = pickle.load( open(authors_file, "r") )



## test_size is the percentage of events assigned to the test set (the
## remainder go into training)
### feature matrices changed to dense representations for compatibility with
### classifier functions in versions 0.15.2 and earlier
#### with .toarray() in features_test  = vectorizer.transform(features_test)
####    and after features_train = features_train[:150]
from sklearn import cross_validation
features_train, features_test, labels_train, labels_test = (
    cross_validation.train_test_split(
        word_data, authors, test_size=0.1, random_state=42))

from sklearn.feature_extraction.text import TfidfVectorizer
# sublinear_tf Applies sublinear tf scaling, i.e. replace tf with 1 + log(tf).
# Not sure why this is a good idea here (or anywhere really)
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                             stop_words='english')
features_train = vectorizer.fit_transform(features_train)
features_test  = vectorizer.transform(features_test)  # no need to refit???


### a classic way to overfit is to use a small number
### of data points and a large number of features;
### train on only 150 events to put ourselves in this regime
features_train = features_train[:150]
labels_train   = labels_train[:150]



### your code goes here
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
clf = DecisionTreeClassifier()
clf.fit(features_train, labels_train)

# same as print clf.score(features_test, labels_test)
pred = clf.predict(features_test)
print "Accuracy score:"
print accuracy_score(labels_test, pred)
print

IMP_THRESH = 0.2  # importance threshold
from operator import itemgetter
all_feats = vectorizer.get_feature_names()
feature_importances = clf.feature_importances_
imp_features = sorted([(str(all_feats[i]), j) for i, j
                      in enumerate(feature_importances)
                      if j > IMP_THRESH],
                      reverse = True, key=itemgetter(1))
print "Words in order of importance value:"
print imp_features
