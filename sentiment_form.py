from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField, Form, TextAreaField, validators
from wtforms.validators import DataRequired, Email, Length

class ReviewForm(Form):
    text_review = TextAreaField('',
                                [validators.DataRequired(),
                                validators.length(min=15)],
                                default = 'I think this app is really cool! :)')