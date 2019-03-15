from flask import render_template, url_for, flash, redirect, request, abort, Blueprint #importing Flask class
from flask_login import current_user, login_required #will handle user log in action
from flaskblog import db
from flaskblog.models import  Post
from flaskblog.posts.forms import PostForm # Importing forms from forms.py here

#Create instance of a blueprint
# 'posts' is the name of blueprint 
posts = Blueprint('posts', __name__) #Similar to creating instance of flask ( app = Flask(__name__) ) but in this case we also passing name of the blueprint ('posts')




    
#New subpage post/new
@posts.route("/post/new", methods=['GET','POST']) # Now we are allowing 'GET' and 'POST' request in this route
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
        return redirect(url_for('main.home')) #Redirect now to home page
    return render_template('create_post.html', title='New Post', form = form, legend = 'New Post') #
    
    
    
#New subpage: 	Create route that will takes us to page for specific post 
#In database each post has an ID (ID is an integer)
@posts.route("/post/<int:post_id>") # 
def post(post_id):
    post = Post.query.get_or_404(post_id) # If we are getting something from database by ID then we neeed to use 'get' method. In this case we will use slightly diffrent method 'get_or_404' - if ID do not exist then return html code 404 (web page do not exist)
    return render_template('post.html', title= post.title, post = post) #

#Route for updating posts - user can update only own posts
#This route will require login 
@posts.route("/post/<int:post_id>/update", methods=['GET','POST']) # 
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
        return redirect(url_for('posts.post', post_id = post.id)) #Redirect now to home page
    #If request.method == 'GET' then populate the forms with username and email
    elif(request.method == 'GET'): 
        form.title.data = post.title #for filling field with current post data
        form.content.data = post.content #for filling field with current post data
    #Now render template
    return render_template('create_post.html', title='Update Post', form = form, legend = 'Update Post') #
    
    
#This route will require login 
@posts.route("/post/<int:post_id>/delete", methods=['POST']) # Only 'POST' request here
@login_required #adding this decoretor - this means that we need to log in in order to access account route
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) 
    #Only user who wrote this post can update/edit this post
    if(post.author != current_user):
        abort(403) # We are doing manual abort here. 403 html response is http for forrbiden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post have been deleted!', 'success') #Add flash message that will tell user that 
    return redirect(url_for('main.home')) #Redirect now to home page
    
