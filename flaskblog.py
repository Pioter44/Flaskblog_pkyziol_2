from flask import Flask, render_template, url_for #importing Flask class


app = Flask(__name__) #Start Flask. Instatation of our Flask in 'app' variable. __name__ is the name of the module. If we run flaskblog.py directly then __name__ will be equal to __main__
                      # By executing this cmd Flask will know where to look for static and template files

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
def hello():
    #return "<h1>Hello WORLD Pkyziol Wolbrom PG 10!<h1>"
    #Passing 'post' dynamic data to html template
    return render_template('home.html', posts= posts)

#New subpage
@app.route("/about")
def about():
    #return "<h1>About me - pkyziol<h1>"
    return render_template('about.html', title = 'About')

# __name__ == '__main__' if we are running this script directly from python script, otherwise is not true
if( __name__ == '__main__'):
    app.run(debug=True)




