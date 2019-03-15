import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager   #Import flask-login extension
from flask_mail import Mail #Import needed for sending mail
from flaskblog.config import Config

app = Flask(__name__) #Start Flask. Instatation of our Flask in 'app' variable. __name__ is the name of the module. If we run flaskblog.py directly then __name__ will be equal to __main__
                      # By executing this cmd Flask will know where to look for static and template files

#Part for inialization of our extensions but without app variable
db = SQLAlchemy() #instance of our SQLAlchemy database (app is an argument for that)
bcrypt = Bcrypt() #Initialize bcrypt for encrypting user password
login_manager = LoginManager()  #Create instance of LoginManager. It will hold on all user sessions in background for us
login_manager.login_view = 'users.login' #Set the login route. 'login' is a function name of the route
login_manager.login_message_category = 'info' #Adding nice flash message 


mail = Mail()


#Creation of our up by function
#   It will allow:  create diffrent instances of our application with diffrent configuration
#   
def create_app(config_class=Config):
    
    #Creation of our app
    app.config.from_object(Config) #
    app.config.update(Config.mail_settings)
    
    #Using init_app method to pass application to all those extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    
    #Lets do import of routes here (after app initialization) to avoid circular importing 
    #Import users
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    
    #Our blueprints
    #Register those users with app
    app.register_blueprint(users)
    #Register those posts with app
    app.register_blueprint(posts)
    #Register those main with app
    app.register_blueprint(main)
    
    
    #At the end return application app that we have created
    return app
    
    