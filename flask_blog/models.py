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
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete') # lazy="select"
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete')
    
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
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_edited = db.Column(db.DateTime) # 這裡應該改成可空且預設為None
    view = db.Column(db.Integer, nullable=False, default=0)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete')
    category = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'Post({self.title}, {self.date_posted}, {self.category})'

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_edited = db.Column(db.DateTime)
    date_deleted = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE')) # 自己reference自己做one to many relation，也要加上foreign key
    reply = db.relationship('Comment', remote_side='Comment.id', backref='replies', lazy=True, cascade='all, delete') # 這裡要設定remote_side，然後傳入class
    likes = db.relationship('Like', backref='comment', lazy=True, cascade='all, delete')
    delete = db.Column(db.Boolean, default=0)
    
    def __repr__(self):
        return f'Comment({self.id}, {self.date_edited})'
    
class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    date_liked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'), nullable=False)