
# Import python modules
import numpy as np
import csv
import matplotlib.pyplot as plt
import nltk
from nltk.stem.porter import *
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
#from sklearn.metrics import roc_curve, auc

#%%
# Part 1: Load data from .csv file
############
with open('movie_reviews.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=',',quotechar='"')

    # Initialize lists for data and class labels
    data =[]
    labels = []
    # For each row of the csv file
    for row in reader:
        # skip missing data
        if row[0] and row[1]:
            data.append(row[0].decode('utf-8'))
            y_label = -1 if row[1]=='negative' else 1
            labels.append(y_label)


#%%
# Part 2: Data preprocessing
############
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
                 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
                 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
                 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
                 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
                 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
punctuation = set(string.punctuation)
stemmer = PorterStemmer()

# For each document in the dataset, do the preprocessing
for doc_id, text in enumerate(data):
    # Remove punctuation and lowercase
    doc = ''.join([w for w in text.lower() if w not in punctuation])

    # Stopword removal
    doc = [w for w in doc.split() if w not in stopwords]

    # Stemming
    doc = [stemmer.stem(w) for w in doc]

    # Convert list of words to one string
    doc = ' '.join(w for w in doc)
    data[doc_id] = doc   # list data contains the preprocessed documents


#%%
# Part 3: Feature extraction and the TF-IDF matrix
#############
m = TfidfVectorizer()
tfidf_matrix = m.fit_transform(data)
tfidf_matrix = tfidf_matrix.toarray()
print "Size of TF-IDF matrix: ", tfidf_matrix.shape


#%%
# Part 4: Model learning and prediction
#############
## Split the data into random train and test subsets. Here we use 40% of the
# data for testing)
data_train, data_test, labels_train, labels_test = cross_validation.train_test_split(
                        tfidf_matrix, labels, test_size=0.4, random_state=42)


## Model learning and prediction
"""clf_nb = BernoulliNB()
y_score = clf_nb.fit(data_train, labels_train).predict_proba(data_test)
labels_predicted = clf_nb.predict(data_test)

clf_log = LogisticRegression()
y_score = clf_log.fit(data_train, labels_train).predict_proba(data_test)
labels_predicted = clf_log.predict(data_test)

clf_forest = RandomForestClassifier(max_depth=10)
y_score = clf_forest.fit(data_train, labels_train).predict_proba(data_test)
labels_predicted = clf_forest.predict(data_test)"""

parameters = [
        {'kernel':['rbf'], 'C':[1, 2, 4, 8, 16, 32, 100], 'gamma':[1, 0.5, 0.1, 0.01, 0.001]}
    ]

#{'kernel': 'rbf', 'C': 2, 'gamma': 0.5}

svm = SVC()
clf_svm = GridSearchCV(svm, parameters)
y_score = clf_svm.fit(data_train, labels_train)
labels_predicted = clf_svm.predict(data_test)
print clf_svm.best_params_

#### Evaluation of the prediction
print classification_report(labels_test, labels_predicted)
print "The accuray score is {:.2%}".format(accuracy_score(labels_test, labels_predicted))
