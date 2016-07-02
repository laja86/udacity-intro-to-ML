#!/usr/bin/python

import os
import pickle
import re
import sys

sys.path.append( "../tools/" )
from parse_out_email_text import parseOutText
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from copy import deepcopy

"""
    Starter code to process the emails from Sara and Chris to extract
    the features and get the documents ready for classification.

    The list of all the emails from Sara are in the from_sara list
    likewise for emails from Chris (from_chris)

    The actual documents are in the Enron email dataset, which
    you downloaded/unpacked in Part 0 of the first mini-project. If you have
    not obtained the Enron email corpus, run startup.py in the tools folder.

    The data is stored in lists and packed away in pickle files at the end.
"""

# from_person.txt contains newline-separated list of paths to relevant emails
from_sara  = open("from_sara.txt", "r")
from_chris = open("from_chris.txt", "r")

from_data = []  # labels, encoded to 0 or 1 depending on the email author
word_data = []  # features, preprocessed email text

### temp_counter is a way to speed up the development--there are
### thousands of emails from Sara and Chris, so running over all of them
### can take a long time
### temp_counter helps you only look at the first 200 emails in the list so you
### can iterate your modifications quicker
temp_counter_disabled = True
temp_counter = 0

# outer loop iterates over (name, open file) for each person
for name, from_person in [("sara", from_sara), ("chris", from_chris)]:
    for path in from_person:  # loops over file, reading each line (efficient)
        ### only look at first 200 emails when developing
        ### once code is working, remove this line to run over full dataset
        if not temp_counter_disabled:
            temp_counter += 1
        # inefficient? iterates through all paths, but only opens limited
        #   number of emails. Could just iterate through that many paths
        if temp_counter < 200 or temp_counter_disabled:
            path = os.path.join('..', path[:-1])  # not sure what this does
            # # returns output of email directory, for reference (??)
            # print path
            email = open(path, "r")  # opens email file

            ### use parseOutText to extract the text from the opened email
            preprocessed_email = parseOutText(email)

            ### use str.replace() to remove any instances of the words
            ### ["sara", "shackleton", "chris", "germani"] i.e. signature words
            signature_words = ["sara", "shackleton", "chris", "germani"]
            for s in signature_words:
                preprocessed_email = preprocessed_email.replace(s, '')

            ### append the text to word_data
            word_data.append(preprocessed_email)

            ### append a 0 to from_data if email is from Sara,
            ###     and 1 if email is from Chris
            from_data.append(0 if name == "sara" else 1)

            email.close()

print "emails processed"
from_sara.close()
from_chris.close()

pickle.dump( word_data, open("your_word_data.pkl", "w") )
pickle.dump( from_data, open("your_email_authors.pkl", "w") )

### in Part 4, do TfIdf vectorization here
#   Using min_df=1 (default), which is cutoff for inclusion based on frequency

# Method 1: using sklearn's stopword list as keyword argument
#   Note that 'english' is only valid keyword argument value at this time
# Gives correct result for quiz
vectorizer = TfidfVectorizer(stop_words='english')
# assigning return val of fit_transform() not required
#   not sure how to use the returned tf_idf_matrix (yet)
tf_idf_matrix = vectorizer.fit_transform(word_data)
print "word data vectorized with method 1"
print "num features:", len(vectorizer.get_feature_names())

# methods commented out below use nltk's stopwords, but can't get it to work
#   can try later with different methods and testing.


# # Method 2: using nltk's stopword list as keyword argument
# sw = stopwords.words('english')
# vectorizer2 = TfidfVectorizer(stop_words=sw)
# tf_idf_matrix2 = vectorizer2.fit_transform(word_data)
# print "word data vectorized with method 2"
# print "num features:", len(vectorizer2.get_feature_names())
#
# # Method 3: use nltk's stopword list to manually remove stopwords
# word_data_manually_processed = deepcopy(word_data)
# for wd in word_data_manually_processed:
#     for s in sw:
#         wd = wd.replace(s, '')
# # Could not get nested list comprehension below to work
# # word_data2 = [wd.replace(s, '')
# #               for wd in word_data
# #               for s in sw]
# vectorizer3 = TfidfVectorizer(stop_words=None)  # default kwarg value
# tf_idf_matrix3 = vectorizer3.fit_transform(word_data_manually_processed)
# print "word data vectorized with method 3"
# print "num features:", len(vectorizer3.get_feature_names())
