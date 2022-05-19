from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,StringField,SelectField
from wtforms.validators import DataRequired

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Add your Bio',validators = [DataRequired()])
    submit = SubmitField('Submit')
    
    
class BlogForm(FlaskForm):
    blog_title = StringField('Blog title', validators=[DataRequired()])
    category = SelectField('Blog category',choices=[('Select a category','Select a category'),('Adventure', 'Adventure'),('Food','Food'),('Music','Music'),('Fashion','Fashion')], validators=[DataRequired()])
    content = TextAreaField('Body', validators=[DataRequired()])
    created_by= StringField('Blog author',validators=[DataRequired()])
    submit = SubmitField('Submit')    
    
    
class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    bio = TextAreaField('About...', validators=[DataRequired()])
    submit = SubmitField('Submit')    
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Write your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')    