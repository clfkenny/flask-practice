from flask import Flask, render_template, request, session, redirect, url_for

from sentiment_form import ReviewForm
from load_models import load_sentiment_model

import numpy as np
import sklearn


###
from flask import Flask, render_template,request
#scientific computing library for saving, reading, and resizing images
from scipy.misc import imsave, imread, imresize
#for matrix math
import numpy as np
#for importing our keras model
import keras.models
#for regular expressions, saves time dealing with string data
import re
import base64
#system level operations (like loading files)
import sys 
#for reading operating system data
import os
#tell our app where our saved model is
sys.path.append(os.path.abspath("model"))
from load import * 

global model, graph
#initialize these variables
model, graph = init()

def convertImage(imgData1):
    imgstr = re.search(b'base64,(.*)',imgData1).group(1)
    #print(imgstr)
    with open('output.png','wb') as output:
        output.write(base64.b64decode(imgstr))
    
###


app = Flask(__name__)



clf, vect = load_sentiment_model()

def classify(document):
    label = {0: 'negative', 1: 'positive'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))
    return label[y], proba



@app.route("/")
def index():
    #form = ReviewForm(request.form)
    return render_template("index.html")

@app.route("/text_sentiment")
def text_sentiment():
    form = ReviewForm(request.form)
    return render_template('text_sentiment.html', form = form)


@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['text_review']
        y, proba = classify(review)
        return render_template('results.html',
                                content=review,
                                prediction=y,
                                probability=round(proba*100, 2))
    return render_template('text_sentiment.html', form=form)


@app.route('/digits')
def digit_classifiy():
    return render_template('digits.html')

@app.route('/predict/',methods=['GET','POST'])
def predict():
    #whenever the predict method is called, we're going
    #to input the user drawn character as an image into the model
    #perform inference, and return the classification
    #get the raw data format of the image
    imgData = request.get_data()
    #encode it into a suitable format
    convertImage(imgData)
    print("debug")
    #read the image into memory
    x = imread('output.png',mode='L')
    #compute a bit-wise inversion so black becomes white and vice versa
    x = np.invert(x)
    #make it the right size
    x = imresize(x,(28,28))
    #imshow(x)
    #convert to a 4D tensor to feed into our model
    x = x.reshape(1,28,28,1)
    print ("debug2")
    #in our computation graph
    with graph.as_default():
        #perform the prediction
        out = model.predict(x)
        print(out)
        print(np.argmax(out,axis=1))
        print("debug3")
        #convert the response to a string
        response = np.array_str(np.argmax(out,axis=1))
        return response 
    

if __name__ == "__main__":
    app.run(debug=True)
