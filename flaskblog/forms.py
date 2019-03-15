from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # for user profile picture. FileField is a type o field and FileAllowed is like validator (list of allowed extensions of image file)
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField #
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

    #This class will be for enabling for user the change (update) of username and mail
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profice Picture', validators =[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    #Add our custom validation method for checking if username or email that user want to change is already in db
    #For update of username and mail we want to run those validators only when new user name or new email is diffrent than currect user name or email 
    def validate_username(self, username):
        if(username.data!=current_user.username):
            user= User.query.filter_by(username=username.data).first()
            if(user):
                raise ValidationError('That username is taken. Please choose a diffrent one')
    
    def validate_email(self, email):
        if(email.data!=current_user.email):
            user= User.query.filter_by(email=email.data).first()
            if(user):
                raise ValidationError('That email is taken. Please choose a diffrent one')
            
#New form for create_post. This form will have two fields 
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()]) #This field will have title and validators
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')
    
#New form for Password Reset (For ResetPassword Page)
#Inherit from FlaskForm
class RequestResetForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    submit = SubmitField('Request Password Reset')
    
    #Method for validate email
    def validate_email(self, email):
        user= User.query.filter_by(email=email.data).first()
        if(user is None):
            raise ValidationError('There is no account with that email. You must register first.')

#New form for Password Reset (For ResetPassword Page)
#Inherit from FlaskForm
class ResetPasswordForm(FlaskForm): 
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    