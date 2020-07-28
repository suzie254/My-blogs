from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

class NewBlogForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    content = TextAreaField('Content', validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Submit')