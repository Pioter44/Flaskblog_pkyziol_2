import os
import secrets #This lib will be used to change picture name to unique hashed string
from PIL import Image #for resizing picture
from flask import render_template, url_for, flash, redirect, request, abort #importing Flask class
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm # Importing forms from porms.py here
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required #will handle user log in action
from flask_mail import Message

#Now almost all webpages have dynamic data (not static)
# - dynammic data are: posts, pictures placed by users on website
#Declaring data structure (list of dicts) that will be used to put dynamic data
'''
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
'''
 

@app.route("/") #route decorator. This decoreator allows to add aditional subpages. Decorators allows to add aditional functionality to existing functions
@app.route("/home")
def home():
    #return "<h1>Hello WORLD Pkyziol Wolbrom PG 10!<h1>"
    #posts = Post.query.all() #create post variable that will have query for all post
    page = request.args.get('page', 1, type=int) # default page is page '1', type int is for 
    #posts = Post.query.paginate(page=page, per_page=5) #create post variable that will use paginate
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #create post variable that will use paginate and order posts (latest first)
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
    
    
#New subpage post/new
@app.route("/post/new", methods=['GET','POST']) # Now we are allowing 'GET' and 'POST' request in this route
@login_required #adding this decoretor - this means that we need to log in in order to access account route
def new_post():
    form = PostForm() #create instance of our PostForm
    #Add condition if our form is valid during submission (this is for 'POST' request)
    if (form.validate_on_submit()):
        #get post from our form and save it to db
        post = Post(title= form.title.data, content= form.content.data, author=current_user)
        db.session.add(post) #Add post to db
        db.session.commit() #Commit (save) post to db
        flash('Your post have been created!', 'success') #Add flash message that will tell user that 
        return redirect(url_for('home')) #Redirect now to home page
    return render_template('create_post.html', title='New Post', form = form, legend = 'New Post') #
    
    
    
#New subpage: 	Create route that will takes us to page for specific post 
#In database each post has an ID (ID is an integer)
@app.route("/post/<int:post_id>") # 
def post(post_id):
    post = Post.query.get_or_404(post_id) # If we are getting something from database by ID then we neeed to use 'get' method. In this case we will use slightly diffrent method 'get_or_404' - if ID do not exist then return html code 404 (web page do not exist)
    return render_template('post.html', title= post.title, post = post) #

#Route for updating posts - user can update only own posts
#This route will require login 
@app.route("/post/<int:post_id>/update", methods=['GET','POST']) # 
@login_required #adding this decoretor - this means that we need to log in in order to access account route
def update_post(post_id):
    post = Post.query.get_or_404(post_id) 
    #Only user who wrote this post can update/edit this post
    if(post.author != current_user):
        abort(403) # We are doing manual abort here. 403 html response is http for forrbiden route
    form = PostForm() #create instance of our PostForm
    #This if is for writing updated/edited post to db (if statment is checking if data are correct)
    if (form.validate_on_submit()):
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() #Commit (save) post to db. We dont need to do db.session.add because data are already in db and we are only doing data update
        flash('Your post have been updated!', 'success') #Add flash message that will tell user that 
        return redirect(url_for('post', post_id = post.id)) #Redirect now to home page
    #If request.method == 'GET' then populate the forms with username and email
    elif(request.method == 'GET'): 
        form.title.data = post.title #for filling field with current post data
        form.content.data = post.content #for filling field with current post data
    #Now render template
    return render_template('create_post.html', title='Update Post', form = form, legend = 'Update Post') #
    
    
#This route will require login 
@app.route("/post/<int:post_id>/delete", methods=['POST']) # Only 'POST' request here
@login_required #adding this decoretor - this means that we need to log in in order to access account route
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) 
    #Only user who wrote this post can update/edit this post
    if(post.author != current_user):
        abort(403) # We are doing manual abort here. 403 html response is http for forrbiden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post have been deleted!', 'success') #Add flash message that will tell user that 
    return redirect(url_for('home')) #Redirect now to home page
    
    
    
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int) # default page is page '1', type int is for 
    user = User.query.filter_by(username = username).first_or_404() #If you will get None then return code 404
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) #create post variable that will use paginate and order posts (latest first)
    #Passing 'post' dynamic data to html template
    return render_template('user_posts.html', posts= posts, user=user)
    
#Method that will handle sending email to a user
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients = [user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token = token, _external=True)}

If you did not make this request then simply ignore this email and no change will be done.
    '''
    #Send mail
    mail.send(msg)
    
#New subpage/route where user will request to reset passowrd
#New subpage/route where user enter email address where rest password information should be sent. URL for this website will be "/reset_password"
@app.route("/reset_password", methods=['GET','POST']) # Now we are allowing 'GET' and 'POST' request in this route
def reset_request():
    #This if is to make sure that user is "LOG OUT" before reseting their password
    if current_user.is_authenticated:
        return redirect(url_for('home')) #if user is "LOG IN" then redirect to home page (only user that is not "LOG IN" can reset password)
    
    form = RequestResetForm() #create instance of our RequestResetForm
    #After we created our form we need to validate if the submited form was correct
    if(form.validate_on_submit()):
        #At that point user submited email in the form so lets check if we have user for such email in db
        user = User.query.filter_by(email = form.email.data).first() # .first() means that we need first user with that email
        #Now we are going to send email to that user with a token that they can use to reset their password
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info') #Add flash message that will tell user that 
        #Now redirect user to 'login' webpage
        return redirect(url_for('login')) 
        
    return render_template('reset_request.html', title= 'Reset Password', form=form) #render the template
    
    
    
#New subpage/route where user will acctually reset/change the password. 
#We need to make sure that token that we gave to user in email is valid.
#By sending user an email with a link containg this token we will know that it's them when they navigate to this route
#URL for this website will be "/reset_password/<token>". Accept token as a parameter
@app.route("/reset_password/<token>", methods=['GET','POST']) # Now we are allowing 'GET' and 'POST' request in this route
def reset_token(token):
    #This if is to make sure that user is "LOG OUT" before reseting their password
    if current_user.is_authenticated:
        return redirect(url_for('home')) #if user is "LOG IN" then redirect to home page (only user that is not "LOG IN" can reset password)
    
    user = User.verify_reset_token(token) #Validate if the token is valid by using method 'verify_reset_token' from User class. Here we are passing token from URL
    if(user is None):
        #Here 'token' is not valid and we are going to return 'reset_request.html'
        flash('That is an invalid or expired token', 'warning') #Add flash message that will tell user that 
        return render_template('reset_request.html') #render the template
    
    #Here 'token' is valid and we are going to return 'reset_token.html'
    form = ResetPasswordForm() #create instance of our RequestResetForm
    
    #Putting some checkers to check if values that we have put are correct (valid) or not
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash user password
        user.password = hashed_password
        db.session.commit() #Commit changes to db
        flash(f'Your password has been updated. You are now able to log in!', 'success')#Sending flash message (flash message is for one time warning message). Flash() function accept two arguments
        return redirect(url_for('login')) #If successful then redirect user to home page
    
    return render_template('reset_token.html', title= 'Reset Password', form=form) #render the template
    
    
    