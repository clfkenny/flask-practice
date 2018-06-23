import pickle
import re
import os

clf = pickle.load(open(os.path.join('movieclassifier/pkl_objects', 'classifier.pkl'), 'rb'))
vect = pickle.load(open(os.path.join('movieclassifier/pkl_objects', 'vect.pkl'), 'rb'))

import numpy as np
label = {0: 'negative', 1:'positive'}
example = ['I love this movie']
X = vect.transform(example)
print('Prediction: %s\nProbability: %.2f%%' %\
      (label[clf.predict(X)[0]],
       np.max(clf.predict_proba(X))*100))
