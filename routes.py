from flask import Flask, render_template, request, session, redirect, url_for
# from models import db, User
from forms import ReviewForm
import pickle
import sqlite3
import os
import numpy as np
import sklearn


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
# db.init_app(app)

# app.secret_key = "development-key"
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
                 'movieclassifier/pkl_objects',
                 'classifier.pkl'), 'rb'))
vect = pickle.load(open(os.path.join(cur_dir,
                 'movieclassifier/pkl_objects',
                 'vect.pkl'), 'rb'))

def classify(document):
    label = {0: 'negative', 1: 'positive'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))
    return label[y], proba



@app.route("/")
def index():
    form = ReviewForm(request.form)
    return render_template("index.html", form = form)


@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['moviereview']
        y, proba = classify(review)
        return render_template('results.html',
                                content=review,
                                prediction=y,
                                probability=round(proba*100, 2))
    return render_template('index.html', form=form)


# @app.route("/about")
# def about():
#   return render_template("about.html")

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#   if 'email' in session:
#     return redirect(url_for('home'))

#   form = SignupForm()

#   if request.method == "POST":
#     if form.validate() == False:
#       return render_template('signup.html', form=form)
#     else:
#       newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
#       db.session.add(newuser)
#       db.session.commit()

#       session['email'] = newuser.email
#       return redirect(url_for('home'))

#   elif request.method == "GET":
#     return render_template('signup.html', form=form)

# @app.route("/login", methods=["GET", "POST"])
# def login():
#   if 'email' in session:
#     return redirect(url_for('home'))

#   form = LoginForm()

#   if request.method == "POST":
#     if form.validate() == False:
#       return render_template("login.html", form=form)
#     else:
#       email = form.email.data 
#       password = form.password.data 

#       user = User.query.filter_by(email=email).first()
#       if user is not None and user.check_password(password):
#         session['email'] = form.email.data 
#         return redirect(url_for('home'))
#       else:
#         return redirect(url_for('login'))

#   elif request.method == 'GET':
#     return render_template('login.html', form=form)

# @app.route("/logout")
# def logout():
#   session.pop('email', None)
#   return redirect(url_for('index'))

# @app.route("/home", methods=["GET", "POST"])
# def home():
#   if 'email' not in session:
#     return redirect(url_for('login'))

#   return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)