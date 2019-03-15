from flask import Blueprint, render_template

#Create new Blueprint instance for error
#If we creating new Blueprint then we need to give names ('errors') and also this variable __name__ 
errors = Blueprint('errors', __name__)


#app_errorhandler is a method that can work in entaire application 
#This decorator will be a handler for 404 errors
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404 # return in flask can return 2 values (render template and status code. The default vale for status code is 200)
    
    

#This decorator will be a handler for 403 errors
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403 # return in flask can return 2 values (render template and status code. The default vale for status code is 200)
    
    

#This decorator will be a handler for 500 errors
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500 # return in flask can return 2 values (render template and status code. The default vale for status code is 200)
    
    