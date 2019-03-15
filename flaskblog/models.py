from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #It will help to handle expiration of tokens during request of password reseting
from flaskblog import db, login_manager, app # import db because class User and Post are using it. app will be used by functions related to "user password reset"
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
    
    #This method will help to create tokens that will be helpful during request of password reseting by user 
    #Example from console:
    #>>>
    #>>> s= Serializer('secret1',60)
    #>>> token = s.dumps({'user_id': 1}).decode('utf-8') # This is a payload: {'user_id': 1}
    #>>> token
    #'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU1MjU1OTI4MSwiZXhwIjoxNTUyNTU5MzQxfQ.eyJ1c2VyX2lkIjoxfQ.b8kf8Z_94td1WqvrRaA60yJV9814-L98jEYtMPL-q_R7jpZPzmDd_Q6fULQM44k-bhl-8wMDaiQdw_TBsXS5GQ'
    #>>> s.loads(token)
    #{'user_id': 1}
    #>>>
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec) #use app SECRET_KEY (it is in __init__.py)
        return s.dumps({'user_id': self.id}).decode('utf-8') #User will be an instance of this user (self.id). This 'return' return token that is created by dumps method that have payload of current user id
    
    
    #Method that will verify token. This method is taking as an input a token calculated by get_reset_token(self, expires_sec=1800)
    @staticmethod #Using decoretor here (staticmethod) because we want to tell that this method will not use 'self' as an argument
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY']) #Create selializer object again with this 'SECRET_KEY'. We dont need to pass expires_sec this time
        #Use try because token can be invalid (for example expired with time grater than 'expires_sec' time)
        try:
            user_id = s.loads(token)['user_id'] # Check if token is valid (token valid: {'user_id': 1}; token not valid: itsdangerous.exc.SignatureExpired: Signature expired)
        except:
            return None
        return User.query.get(user_id) #Return User with that ID
        
    
    
    
    
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
    