from datetime import datetime
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect #importing Flask class


app = Flask(__name__) #Start Flask. Instatation of our Flask in 'app' variable. __name__ is the name of the module. If we run flaskblog.py directly then __name__ will be equal to __main__
                      # By executing this cmd Flask will know where to look for static and template files

#Set secret key for our application. Secret Key will prevent from modifing our cookies and cross-side attacs
app.config['SECRET_KEY'] = '4e21f3a3cafa9ba6913d728def0db6f7'

#SQLlite DB will be a file on our file system
#We need to specify URI where our database will be located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #site.db should be created alongsite our other files in our current working directory

db = SQLAlchemy(app) #instance of our SQLAlchemy database (app is an argument for that)

#For SQLAlchemy DB we can have represent database structure as a classes. Those classes will be a modules
#Each class will be an own table in database 
#User class to hold users (inheriting from db.Model)
class User(db.Model):
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
    
#Now almost all webpages have dynamic data (not static)
# - dynammic data are: posts, pictures placed by users on website
#Declaring data structure (list of dicts) that will be used to put dynamic data
posts = [
    {
    'author' : 'Corey Schafer',
    'title' : 'Blog Post 1',
    'content' : 'First post content',
    'date_posted' : 'April 20, 2018'
    },
    {
    'author' : 'Piotr Kyziol',
    'title' : 'Blog Post 2',
    'content' : 'Second post content',
    'date_posted' : 'April 21, 2018'
    }

]
 
 

@app.route("/") #route decorator. This decoreator allows to add aditional subpages. Decorators allows to add aditional functionality to existing functions
@app.route("/home")
def home():
    #return "<h1>Hello WORLD Pkyziol Wolbrom PG 10!<h1>"
    #Passing 'post' dynamic data to html template
    return render_template('home.html', posts= posts)

#New subpage
@app.route("/about")
def about():
    #return "<h1>About me - pkyziol<h1>"
    return render_template('about.html', title = 'About')

#New subpage registration
@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    #Putting some checkers to check if values that we have put are correct (valid) or not
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')#Sending flash message (flash message is for one time warning message). Flash() function accept two arguments
        return redirect(url_for('home')) #If successful then redirect user to home page
    return render_template('register.html', title='Register', form = form)
    
#New subpage login
@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    #Putting some checkers to check if values that we have put are correct (valid) or not
    if form.validate_on_submit():
        if (form.email.data == 'admin@blog.com' and form.password.data == "1234"): #This is temporary simulation of succesful login
            flash('You have been login', 'success')
            return redirect(url_for('home')) #If successful then redirect user to home page
        else:
            flash('Login Unsuccesfull. Pls check username and password', 'danger') #Use bootstrap class 'danger' for this alert
    return render_template('login.html', title='Login', form = form)
    
    
# __name__ == '__main__' if we are running this script directly from python script, otherwise is not true
if( __name__ == '__main__'):
    app.run(debug=True)




