from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.errors.errors_handler import errors
from flask_migrate import Migrate
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect # for image upload protection
from flask_ckeditor import CKEditor
from flask_blog.config import Config
import re

# 根據flask官方所述，把這些extension建立在外面，不直接放入app作為建立的對象，能讓這些extension不被binding在一個物件上
db = SQLAlchemy() # create SQLAlchemy(databese) instance
bcrypt = Bcrypt() # create Bcrypt instance
login_manager = LoginManager() # create LoginManager instance
mail = Mail() # create Main instance
migrate = Migrate()
moment = Moment()
csrf = CSRFProtect()
ck = CKEditor()

#創建一個jinja的filter
def tagify(text):
    return re.sub(r'@([a-zA-Z0-9_]+)\s', r'<a href="/user/\1" style="text-decoration:none;">@\1</a> ', text)
    # \1代表使用這名稱
    
def create_app(config_class=Config):
    
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config_class)
    app.jinja_env.filters['tagify'] = tagify # 註冊這個filter，名稱就叫tagify
    
    # 放在這裡建立
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login' # 讓login manager知道說如果沒有登入的話，要導入至哪個view
    login_manager.login_message_category = 'info' # 顯示導入資訊時的bootstrap category
    mail.init_app(app)
    migrate.init_app(app, db) # it takes two arguments
    moment.init_app(app)
    csrf.init_app(app)
    ck.init_app(app)
    
    # 放在這邊以免產生 circular import/ not found，因為這些package都需要從這裡import db等等東西，所以要先等他們被instantiate
    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    from flask_blog.comments.routes import comments
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(comments)
    
    return app