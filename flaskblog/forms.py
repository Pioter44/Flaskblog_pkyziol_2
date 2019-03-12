from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

#Need to use secret key for those RegistrationForm and LoginForm. Secret Key will prevent from attacs

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    #Add our custom validation method for checking if username or email that user want to register is already in db
    def validate_username(self, username):
        user= User.query.filter_by(username=username.data).first()
    
        if(user):
            raise ValidationError('That username is taken. Please choose a diffrent one')
    
    def validate_email(self, email):
        user= User.query.filter_by(email=email.data).first()
    
        if(user):
            raise ValidationError('That email is taken. Please choose a diffrent one')
            
#Class for Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) #use email as a login name because email is less likely to forget than login
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  #Add to field to stay login for some time when page is closed in browser by using secure cookie. This will be boolen field
    submit = SubmitField('Login')

