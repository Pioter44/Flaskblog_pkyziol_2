from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) #Start Flask. Instatation of our Flask in 'app' variable. __name__ is the name of the module. If we run flaskblog.py directly then __name__ will be equal to __main__
                      # By executing this cmd Flask will know where to look for static and template files

#Set secret key for our application. Secret Key will prevent from modifing our cookies and cross-side attacs
app.config['SECRET_KEY'] = '4e21f3a3cafa9ba6913d728def0db6f7'

#SQLlite DB will be a file on our file system
#We need to specify URI where our database will be located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #site.db should be created alongsite our other files in our current working directory

db = SQLAlchemy(app) #instance of our SQLAlchemy database (app is an argument for that)

#Lets do import of routes here (after app initialization) to avoid circular importing 
from flaskblog import routes
