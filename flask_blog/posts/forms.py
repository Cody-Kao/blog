from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):
    
    title = StringField('Title', validators=[DataRequired()])
    
    category = SelectField('Category', choices=['Travel', 'Food', 'Style'], validators=[DataRequired()])
    
    content = CKEditorField('Content', validators=[DataRequired()])
    
    submit = SubmitField('Post')

class Update_PostForm(FlaskForm): # 新增這個form的原因是要把category這個表單元素拿掉，因為如果用含有category的表的會有一個奇怪的bug，就是在submit update post的時候過不了驗證
    
    title = StringField('Title', validators=[DataRequired()])
    
    content = CKEditorField('Content', validators=[DataRequired()])
    
    submit = SubmitField('Post')