from flask import render_template, url_for, flash, redirect, request, Blueprint #importing Flask class
from flask_login import login_user, current_user, logout_user, login_required #will handle user log in action
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm # Importing forms from porms.py here
from flaskblog.users.utils import save_picture, send_reset_email



#Create instance of a blueprint
# 'users' is the name of blueprint 
users = Blueprint('users', __name__) #Similar to creating instance of flask ( app = Flask(__name__) ) but in this case we also passing name of the blueprint ('users')

#We are no loger use global app to create routes. Instead we are going to creates routes that are specific to this blueprint and register with our application later 
#New subpage registration
#@app.route("/register", methods=['GET','POST'])
@users.route("/register", methods=['GET','POST'])
def register():
    #if user is not "log in" then redirect it to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    #Putting some checkers to check if values that we have put are correct (valid) or not
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash user password
        user = User(username=form.username.data, email=form.email.data, password= hashed_password) #Create new instance of the user
        db.session.add(user) #Add user to db
        db.session.commit() #Commit (save) user to db
        flash(f'Your account have been created. You are now able to log in!', 'success')#Sending flash message (flash message is for one time warning message). Flash() function accept two arguments
        return redirect(url_for('users.login')) #If successful then redirect user to home page
    return render_template('register.html', title='Register', form = form)
    

    
#New subpage login
@users.route("/login", methods=['GET','POST'])
def login():
    #if user is not "log in" then redirect it to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    #Putting some checkers to check if values that we have put are correct (valid) or not
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # Check if user exist
        if( user and bcrypt.check_password_hash(user.password, form.password.data)):
            #If username in db and password is matching then log in user using login_user
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #This line is to eliminate 'next' from the link http://127.0.0.1:5000/login?next=%2Faccount
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccesfull. Pls check username and password', 'danger') #Use bootstrap class 'danger' for this alert
    return render_template('login.html', title='Login', form = form)
    
#New subpage logout
@users.route("/logout")
def logout():
    logout_user()
    #when the user is log out then redirect it to home page
    return redirect(url_for('main.home'))
    
    

    
#New subpage account (Create route for user account that user can access when is log in)
@users.route("/account", methods=['GET','POST'])  #Allowing GET and POST requests
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
        return redirect(url_for('users.account')) #Redirect now to account page
    #It will be nice if our form will be already populated will username data and email. This if is for this purpose
    #If request.method == 'GET' then populate the forms with username and email
    elif(request.method == 'GET'): 
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file) # user images will be located in static/profile_pics folder 
    return render_template('account.html', title='Account', image_file= image_file, form = form) #pass form to our account.html template
    
    
    
    
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int) # default page is page '1', type int is for 
    user = User.query.filter_by(username = username).first_or_404() #If you will get None then return code 404
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) #create post variable that will use paginate and order posts (latest first)
    #Passing 'post' dynamic data to html template
    return render_template('user_posts.html', posts= posts, user=user)
    
    

#New subpage/route where user will request to reset passowrd
#New subpage/route where user enter email address where rest password information should be sent. URL for this website will be "/reset_password"
@users.route("/reset_password", methods=['GET','POST']) # Now we are allowing 'GET' and 'POST' request in this route
def reset_request():
    #This if is to make sure that user is "LOG OUT" before reseting their password
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) #if user is "LOG IN" then redirect to home page (only user that is not "LOG IN" can reset password)
    
    form = RequestResetForm() #create instance of our RequestResetForm
    #After we created our form we need to validate if the submited form was correct
    if(form.validate_on_submit()):
        #At that point user submited email in the form so lets check if we have user for such email in db
        user = User.query.filter_by(email = form.email.data).first() # .first() means that we need first user with that email
        #Now we are going to send email to that user with a token that they can use to reset their password
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info') #Add flash message that will tell user that 
        #Now redirect user to 'login' webpage
        return redirect(url_for('users.login')) 
        
    return render_template('reset_request.html', title= 'Reset Password', form=form) #render the template
    
    
    
#New subpage/route where user will acctually reset/change the password. 
#We need to make sure that token that we gave to user in email is valid.
#By sending user an email with a link containg this token we will know that it's them when they navigate to this route
#URL for this website will be "/reset_password/<token>". Accept token as a parameter
@users.route("/reset_password/<token>", methods=['GET','POST']) # Now we are allowing 'GET' and 'POST' request in this route
def reset_token(token):
    #This if is to make sure that user is "LOG OUT" before reseting their password
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) #if user is "LOG IN" then redirect to home page (only user that is not "LOG IN" can reset password)
    
    user = User.verify_reset_token(token) #Validate if the token is valid by using method 'verify_reset_token' from User class. Here we are passing token from URL
    if(user is None):
        #Here 'token' is not valid and we are going to return 'reset_request.html'
        flash('That is an invalid or expired token', 'warning') #Add flash message that will tell user that 
        return redirect(url_for('users.reset_request'))
    
    #Here 'token' is valid and we are going to return 'reset_token.html'
    form = ResetPasswordForm() #create instance of our RequestResetForm
    
    #Putting some checkers to check if values that we have put are correct (valid) or not
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hash user password
        user.password = hashed_password
        db.session.commit() #Commit changes to db
        flash(f'Your password has been updated. You are now able to log in!', 'success')#Sending flash message (flash message is for one time warning message). Flash() function accept two arguments
        return redirect(url_for('users.login')) #If successful then redirect user to home page
    
    return render_template('reset_token.html', title= 'Reset Password', form=form) #render the template
    
    