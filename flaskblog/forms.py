from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#Need to use secret key for those RegistrationForm and LoginForm. Secret Key will prevent from attacs

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
#Class for Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) #use email as a login name because email is less likely to forget than login
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  #Add to field to stay login for some time when page is closed in browser by using secure cookie. This will be boolen field
    submit = SubmitField('Login')

