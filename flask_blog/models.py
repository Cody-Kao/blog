from datetime import datetime
from flask_blog import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimestampSigner
from flask import current_app

# user_loader(self, callback)
# param callback: The callback for retrieving a user object.
# 所以我們要設定一個function讓login manager利用id找到user的object以紀錄登入的使用者
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def get_reset_token(self): # 取得token 並包裹payload
        s = TimestampSigner(current_app.config['SECRET_KEY'])
        return s.sign(str(self.id)) # 要轉成string才不會出bug
    
    @staticmethod
    def verify_reset_token(token, expire_time=60): # 確認token之後取得該使用者的id 再用query把該使用者回傳 如果沒有找到使用者則raise exception並回傳None
        s = TimestampSigner(current_app.config['SECRET_KEY'])
        try:
            user_id = s.unsign(token, max_age=expire_time)
        except:
            return None
        return User.query.get(int(user_id))
    
    # 印出User instance時會顯示的內容
    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.image_file})'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'Post({self.title}, {self.date_posted})'

    