from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):
    
    title = StringField('Title', validators=[DataRequired()])
    
    category = SelectField('Category', choices=['Travel', 'Food', 'Style'], validators=[DataRequired()])
    
    content = CKEditorField('Content', validators=[DataRequired()])
    
    submit = SubmitField('Post')