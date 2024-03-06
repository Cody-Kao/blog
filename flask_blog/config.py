import os
# 製造一個config的class，將原本設定的app.config都放進來
# 這樣可以使用繼承或是更有架構的管理所有config
# 原本是 app.config('MAIL_PORT') = 587 ==> 現在包裹成class的方式

class Config:
    
    SECRET_KEY = os.urandom(24) # 或者也可以用secrets.token_hex(16) 產出一個key
    # 讓flash message等等功能使用上更安全, sign session cookies for protection against cookie data tampering
    # 而這個key存成環境變數會更好
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
    
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # 輸入使用者名稱(由環境變數中取得)
    
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # 輸入密碼
    
    CKEDITOR_ENABLE_CSRF = True
    
    CKEDITOR_FILE_UPLOADER = 'posts.upload' # 因為是把這個upload endpoint設定在posts這個blueprint裡，所以要前綴