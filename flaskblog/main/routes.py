from flask import render_template, request, Blueprint #importing Flask class
from flaskblog.models import Post

#Create instance of a blueprint
# 'main' is the name of blueprint 
main = Blueprint('main', __name__) #Similar to creating instance of flask ( app = Flask(__name__) ) but in this case we also passing name of the blueprint ('main')





@main.route("/") #route decorator. This decoreator allows to add aditional subpages. Decorators allows to add aditional functionality to existing functions
@main.route("/home")
def home():
    #return "<h1>Hello WORLD Pkyziol Wolbrom PG 10!<h1>"
    #posts = Post.query.all() #create post variable that will have query for all post
    page = request.args.get('page', 1, type=int) # default page is page '1', type int is for 
    #posts = Post.query.paginate(page=page, per_page=5) #create post variable that will use paginate
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #create post variable that will use paginate and order posts (latest first)
    #Passing 'post' dynamic data to html template
    return render_template('home.html', posts= posts)

#New subpage
@main.route("/about")
def about():
    #return "<h1>About me - pkyziol<h1>"
    return render_template('about.html', title = 'About')
    