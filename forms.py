from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField, Form, TextAreaField, validators
from wtforms.validators import DataRequired, Email, Length

class ReviewForm(Form):
    moviereview = TextAreaField('',
                                [validators.DataRequired(),
                                validators.length(min=15)])