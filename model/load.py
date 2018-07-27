import numpy as np
import keras.models
from keras.models import model_from_json
from scipy.misc import imread, imresize,imshow
import tensorflow as tf


def init_digits(): 
	config = tf.ConfigProto()
	config.gpu_options.per_process_gpu_memory_fraction = 0.3
	sess = tf.Session(config=config)

	json_file = open('model/model.json','r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	#load weights into new model
	loaded_model.load_weights("model/model.h5")
	print("Loaded Model from disk")

	#compile and evaluate loaded model
	loaded_model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
	#loss,accuracy = model.evaluate(X_test,y_test)
	#print('loss:', loss)
	#print('accuracy:', accuracy)
	graph = tf.get_default_graph()

	return loaded_model,graph



def init_sketch():
	print('Loading sketch model...')
	json_file = open('model/sketch_model.json','r')
	loaded_model_json = json_file.read()
	json_file.close()
	sketch_model = model_from_json(loaded_model_json)
	sketch_model.load_weights("model/sketch_weights.hdf5")
	sketch_model.compile(loss='categorical_crossentropy', optimizer = 'adam')
	print('Loaded sketch model.\n')
	graph = tf.get_default_graph()

	return sketch_model, graph
