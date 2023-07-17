from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    
    confirm_password = PasswordField('Comfirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username): # function的名稱是個模板，讓flask能執行你新增的自定義檢查
        user = User.query.filter_by(username=username.data).first() # 如果有找到 則回傳該user，若沒有則回傳None
        if user != None:
            raise ValidationError(f'The username {username.data} has been taken! Please choose a new one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user != None:
            raise ValidationError(f'The email {email.data} has been taken! Please choose a new one.')

class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() # 如果有找到 則回傳該user，若沒有則回傳None
            if user != None:
                raise ValidationError(f'The username {username.data} has been taken! Please choose a new one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user != None:
                raise ValidationError(f'The email {email.data} has been taken! Please choose a new one.')

class RequestResetForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please register first or check again!')
    
class ResetPasswordForm(FlaskForm):
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    
    confirm_password = PasswordField('Comfirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password')