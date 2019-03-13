import os
import secrets #This lib will be used to change picture name to unique hashed string
from PIL import Image #for resizing picture
from flask import render_template, url_for, flash, redirect, request #importing Flask class
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm # Need to use package name here
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required #will handle user log in action

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
    #if user is not "log in" then redirect it to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    #Putting some checkers to check if values that we have put are correct (valid) or not
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash user password
        user = User(username=form.username.data, email=form.email.data, password= hashed_password) #Create new instance of the user
        db.session.add(user) #Add user to db
        db.session.commit() #Commit (save) user to db
        flash(f'Your account have been created. You are now able to log in!', 'success')#Sending flash message (flash message is for one time warning message). Flash() function accept two arguments
        return redirect(url_for('login')) #If successful then redirect user to home page
    return render_template('register.html', title='Register', form = form)
    

    
#New subpage login
@app.route("/login", methods=['GET','POST'])
def login():
    #if user is not "log in" then redirect it to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    #Putting some checkers to check if values that we have put are correct (valid) or not
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # Check if user exist
        if( user and bcrypt.check_password_hash(user.password, form.password.data)):
            #If username in db and password is matching then log in user using login_user
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #This line is to eliminate 'next' from the link http://127.0.0.1:5000/login?next=%2Faccount
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesfull. Pls check username and password', 'danger') #Use bootstrap class 'danger' for this alert
    return render_template('login.html', title='Login', form = form)
    
#New subpage logout
@app.route("/logout")
def logout():
    logout_user()
    #when the user is log out then redirect it to home page
    return redirect(url_for('home'))
    
    
#Save picture function
def save_picture(form_picture):
    #Create random hex that will be a part of our picture name
    random_hex = secrets.token_hex(8)
    f_name, f_ext= os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)
    #Resize picture before saveing it
    output_size = (125,125) #tupel - Set size of output picture that we want (values in pixels)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) #Save image to app.root_path,'static/profile_pics'
    return picture_fn
    
#New subpage account (Create route for user account that user can access when is log in)
@app.route("/account", methods=['GET','POST'])  #Allowing GET and POST requests
@login_required #adding this decoretor - this means that we need to log in in order to access account route
def account():
    form = UpdateAccountForm() #create instance of UpdateAccountForm
    #Add condition if our form is valid during submission (this is for 'POST' request)
    if (form.validate_on_submit()):
        #Add condition to see if there is any picture data. This is not required filed so we need to have this check
        if(form.picture.data):
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() #submit updated username and email to db
        flash('Your account has been updated!', 'success') #Add flash message that will tell user that username nad mail have been updated
        return redirect(url_for('account')) #Redirect now to account page
    #It will be nice if our form will be already populated will username data and email. This if is for this purpose
    #If request.method == 'GET' then populate the forms with username and email
    elif(request.method == 'GET'): 
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file) # user images will be located in static/profile_pics folder 
    return render_template('account.html', title='Account', image_file= image_file, form = form) #pass form to our account.html template
    
    
    