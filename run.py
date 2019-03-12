from flaskblog import app #this import is because we are running app here (this is going to import from __init__.py, app need to exist in __init__.py )

# __name__ == '__main__' if we are running this script directly from python script, otherwise is not true
if( __name__ == '__main__'):  #The only purpose of this is to grab application and run it
    app.run(debug=True)




