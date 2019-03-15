from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField #
from wtforms.validators import DataRequired


#New form for create_post. This form will have two fields 
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()]) #This field will have title and validators
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')
    
