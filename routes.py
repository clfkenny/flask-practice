from flask import Flask, render_template, request, session, redirect, url_for
from flask.json import jsonify
from sentiment_form import ReviewForm
from load_models import load_sentiment_model

import numpy as np
import sklearn

import io
from PIL import Image

import pandas as pd
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

import cv2
# global model, graph
#initialize these variables
digits_model, digits_graph = init_digits()

def convertImage(imgData1):
    imgstr = re.search(b'base64,(.*)',imgData1).group(1)
    #print(imgstr)
    with open('output.png','wb') as output:
        output.write(base64.b64decode(imgstr))
    

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
        return render_template('text_sentiment.html',
                                content=review,
                                prediction=y,
                                probability=round(proba*100, 2), form = form)
    return render_template('text_sentiment.html', form=form)


@app.route('/digits')
def digit_classifiy():
    return render_template('digits.html')

@app.route('/predict_digit',methods=['GET','POST'])
def predict_digit():
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
    with digits_graph.as_default():
        #perform the prediction
        out = digits_model.predict(x)
        print(out)
        print(np.argmax(out,axis=1))
        print("debug3")
        #convert the response to a string
        response = np.array_str(np.argmax(out,axis=1))
        return response 
    


sketch_model, sketch_graph = init_sketch()

import pickle

@app.route('/quickdraw')
def quickdraw():
    return render_template('quickdraw.html')

@app.route('/predict_sketch', methods=['GET', 'POST'])
def predict():
    imgData = request.get_data()

    # debug sketch line width
    # imgstr = re.search(b'base64,(.*)',imgData).group(1)
    # with open('sketch_output.png','wb') as output:
    #     output.write(base64.b64decode(imgstr))

    imgstr = re.search(b'base64,(.*)',imgData).group(1)
    img_bytes = io.BytesIO(base64.b64decode(imgstr))
    img = Image.open(img_bytes)
    x = np.array(img)[:,:,0]

    x = np.invert(x)
    x = imresize(x,(28,28))
    x = x.reshape(1,28,28,1)/255


    with open("class_ids.txt", 'rb') as fp:
        class_idx = pickle.load(fp)

    with sketch_graph.as_default():
        pred = sketch_model.predict(x) 
        class_idx_df = pd.DataFrame({'category':list(class_idx.keys())}).reset_index()
        sorted_probs = pd.DataFrame({'probabilities':pred.ravel()}).sort_values(by = 'probabilities', ascending=False).reset_index() 

        merged = pd.merge(class_idx_df, sorted_probs).sort_values('probabilities', ascending=False).reset_index(drop=True)
        print(merged)


        # response = top_results.to_html(classes = ["table-bordered", 'table-striped', 'table-hover'])
        # return response
        top_results = merged.loc[:,['category', 'probabilities']][:10]
        return jsonify({'labels': top_results.category.tolist(), 'values': top_results.probabilities.tolist()}), 201





@app.route('/better_digits')
def better_digits():
    return render_template('better_digits.html')

@app.route('/predict_better_digits', methods=['GET', 'POST'])
def predict_better_digits():
    imgData = request.get_data()

    # debug sketch line width
    # imgstr = re.search(b'base64,(.*)',imgData).group(1)
    # with open('sketch_output.png','wb') as output:
    #     output.write(base64.b64decode(imgstr))

    imgstr = re.search(b'base64,(.*)',imgData).group(1)
    img_bytes = io.BytesIO(base64.b64decode(imgstr))
    img = Image.open(img_bytes)

    im = np.array(img) 
    r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
    mask = (r==0) & (g == 255 ) & (b ==0)
    im[:,:,:3][mask] = [255,255,255]

    cv2.imwrite('debug1.png', im)

    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    print('imgray shape', im_gray.shape)
    print('im shape', im.shape)
    ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
    _, ctrs, _ = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    rects = [cv2.boundingRect(ctr) for ctr in ctrs]

    print('Found {} objects'.format(len(rects)))

    dim1_list = []
    dim2_list = []
    pred_list = []
    confidence_list = []

    with digits_graph.as_default():

        # try:
        for ind, rect in enumerate(rects):
            print(rect[2],' ' ,rect[3])
            # pred_list[ind] = 'blank'

            dim1 = (rect[0], rect[1])
            dim2 = (rect[0]+rect[2], rect[1] + rect[3])

            dim1_list.append(dim1)
            dim2_list.append(dim2)

            top_leftx = rect[0]
            top_lefty = rect[1]
            width = rect[2]
            height = rect[3]
    

            xdiff = 0
            ydiff = 0 
    
            if width >= height: # if width > height, set height = width to make a square
                xdiff = width-height
                height = width
    
            else: 
                ydiff = height-width
                width = height        
    
    
            farthest_left = rect[0]
            farthest_right = rect[0] + rect[2]
            farthest_top = rect[1]
            farthest_bottom = rect[1]+rect[3]

            xpadding = width//3
            ypadding = height//3
    
            if xpadding + ydiff> top_leftx:
                xpadding = top_leftx 
                ydiff=0
        
            if ypadding + xdiff > top_lefty:
                ypadding = top_lefty 
                xdiff=0

        
    
            roi = im_th[top_lefty - ypadding-xdiff:top_lefty + height + ypadding ,
                top_leftx - xpadding-ydiff:top_leftx + width + xpadding ]


            roi = cv2.resize(roi, (28, 28), interpolation = cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3,3))
            # roi = np.invert(roi)

            nbr = np.argmax(digits_model.predict(roi.reshape((1,28,28,1))))
            pred_list.append(int(nbr))

            model_conf = digits_model.predict(roi.reshape((1,28,28,1))).reshape((10, 1))[nbr]
            confidence_list.append(float(model_conf))

            # cv2.putText(im, str(nbr), (rect[0], rect[1]), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 255, 255), 5)




    print(pred_list)
    # cv2.imwrite('debug2.png',im)

    return jsonify({'dim1_list': dim1_list, 'dim2_list': dim2_list,
     'predictions': pred_list, 'probas': confidence_list}), 201




if __name__ == "__main__":
    app.run(debug=True)
