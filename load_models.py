import pickle
import os


def load_sentiment_model():
	cur_dir = os.path.dirname(__file__)
	clf = pickle.load(open(os.path.join(cur_dir,
	                 'sentiment_classifier/pkl_objects',
	                 'classifier.pkl'), 'rb'))
	vect = pickle.load(open(os.path.join(cur_dir,
	                 'sentiment_classifier/pkl_objects',
	                 'vect.pkl'), 'rb'))
	return clf, vect