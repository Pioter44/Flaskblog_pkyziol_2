import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager   #Import flask-login extension
from flask_mail import Mail #Import needed for sending mail

app = Flask(__name__) #Start Flask. Instatation of our Flask in 'app' variable. __name__ is the name of the module. If we run flaskblog.py directly then __name__ will be equal to __main__
                      # By executing this cmd Flask will know where to look for static and template files

#Set secret key for our application. Secret Key will prevent from modifing our cookies and cross-side attacs
app.config['SECRET_KEY'] = '4e21f3a3cafa9ba6913d728def0db6f7'

#SQLlite DB will be a file on our file system
#We need to specify URI where our database will be located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #site.db should be created alongsite our other files in our current working directory

db = SQLAlchemy(app) #instance of our SQLAlchemy database (app is an argument for that)
bcrypt = Bcrypt(app) #Initialize bcrypt for encrypting user password
login_manager = LoginManager(app)  #Create instance of LoginManager. It will hold on all user sessions in background for us
login_manager.login_view = 'login' #Set the login route. 'login' is a function name of the route
login_manager.login_message_category = 'info' #Adding nice flash message 

#This config is not working and giving error: smtplib.SMTPSenderRefused: (530, b'5.5.1 Authentication Required. Learn more at\n5.5.1  https://support.google.com/mail/?p=WantAuthError v8sm58379lji.51 - gsmtp', 'noreply@demo.com')
'''
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#Email and password (specified in environment variable just for security purposes) from where we will send mails to user
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app) #Initialize our extension with app
'''
#Alternative setting (from: https://www.youtube.com/watch?v=vutyTx7IaAI&list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU&index=73)
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
} 
app.config.update(mail_settings)
mail = Mail(app)




#Lets do import of routes here (after app initialization) to avoid circular importing 
from flaskblog import routes
