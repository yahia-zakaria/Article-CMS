from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileRequired

class AddPostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired(message="Title is required")])
    author = StringField('Author', [DataRequired(message="Author is required")])
    body = TextAreaField('Body', [DataRequired(message="Body is required")])
    image= FileField("Image", [FileRequired(message="Image is required")])
    submit = SubmitField("Post")


class EditPostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired(message="Title is required")])
    author = StringField('Author', [DataRequired(message="Author is required")])
    body = TextAreaField('Body', [DataRequired(message="Body is required")])
    image= FileField("Image")
    submit = SubmitField("Post")    

