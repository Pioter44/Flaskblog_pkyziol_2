from datetime import datetime
from flaskblog import db, login_manager # import db because class User and Post are using it
from flask_login import UserMixin

#For SQLAlchemy DB we can have represent database structure as a classes. Those classes will be a modules
#Each class will be an own table in database 
#User class to hold users (inheriting from db.Model)

#Create function with decorator. This is for reloading user with user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #user ID is an integer and this will be our pirimary_key
    username = db.Column(db.String(20), unique=True, nullable=False) #we assumed that username will be max 20 character long. username must be unique and cannot have value NULL
    email = db.Column(db.String(120), unique=True, nullable=False) #we assumed that email will be max 120 character long. email must be unique and cannot have value NULL
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #we assumed that user profile picture name will be max 20 character long. 
    password = db.Column(db.String(60), nullable=False)
    #Post model and User model have relationship since user is an author for a posts (one to many relationship because one user can have multiple posts but posts can have only one author)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    #Special Doonder method for printing out User
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
#Post class to hold users posts (inheriting from db.Model)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) #
    title = db.Column(db.String(100), nullable=False) 
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow) # datetime.utcnow is without parenthis () because we want to pass function (not a value of this executed function)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    #Special Doonder method for printing out post
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    