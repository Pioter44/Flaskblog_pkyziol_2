import os
import secrets #This lib will be used to change picture name to unique hashed string
from PIL import Image #for resizing picture
from flask import url_for, current_app #importing Flask class
from flask_mail import Message
from flaskblog import mail


#Save picture function
def save_picture(form_picture):
    #Create random hex that will be a part of our picture name
    random_hex = secrets.token_hex(8)
    f_name, f_ext= os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics', picture_fn)
    #Resize picture before saveing it
    output_size = (125,125) #tupel - Set size of output picture that we want (values in pixels)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) #Save image to app.root_path,'static/profile_pics'
    return picture_fn
    
    
#Method that will handle sending email to a user
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients = [user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token = token, _external=True)}

If you did not make this request then simply ignore this email and no change will be done.
    '''
    #Send mail
    mail.send(msg)
    