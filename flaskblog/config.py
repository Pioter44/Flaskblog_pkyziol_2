import os

class Config:
    SECRET_KEY = '4e21f3a3cafa9ba6913d728def0db6f7'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' #site.db should be created alongsite our other files in our current working directory
    
    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": os.environ['EMAIL_USER'],
        "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
    } 
    
    '''
    #Set secret key for our application. Secret Key will prevent from modifing our cookies and cross-side attacs
    app.config['SECRET_KEY'] = '4e21f3a3cafa9ba6913d728def0db6f7'

    #SQLlite DB will be a file on our file system
    #We need to specify URI where our database will be located
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #site.db should be created alongsite our other files in our current working directory


    #This config is not working and giving error: smtplib.SMTPSenderRefused: (530, b'5.5.1 Authentication Required. Learn more at\n5.5.1  https://support.google.com/mail/?p=WantAuthError v8sm58379lji.51 - gsmtp', 'noreply@demo.com')

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    #Email and password (specified in environment variable just for security purposes) from where we will send mails to user
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    mail = Mail(app) #Initialize our extension with app

    #Alternative setting (from: https://www.youtube.com/watch?v=vutyTx7IaAI&list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU&index=73)
    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": os.environ['EMAIL_USER'],
        "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
    } 
    app.config.update(mail_settings)
    
     '''