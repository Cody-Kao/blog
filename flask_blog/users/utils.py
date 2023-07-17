import os
import secrets
from flask_mail import Message
from PIL import Image
from flask_blog import mail
from flask import url_for, current_app
from threading import Thread

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # 因為如果單純用使用者輸入的圖檔名稱，可能會撞名，所以隨機產生一個hash當作名稱
    _, f_ext = os.path.splitext(form_picture.filename) # 把圖檔名稱跟檔案格式分開
    picture_fn = random_hex + f_ext # 製造檔名
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # 把整個圖檔存入的路徑寫出來
    
    resize = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(resize) # resize the image
    resized_image.save(picture_path) # 存檔
    
    return picture_fn # 回傳檔名

def write_reset_email(user):
    token = user.get_reset_token()
    # noreply@domain.com這是個不能讓使用者回信的domain，recipients是接受者
    msg = Message('Password Reset Request', sender='noreply@domain.com', recipients=[user.email])
    # 填寫email的內容
    # _external=True 讓產生的連結是絕對路徑，而不是相對(因為不是在我們flask內部打開的)
    msg.body = f"""To reset your password, visit the following link:
{ url_for('users.reset_password', token=token, _external=True) }

#NOTE# You have only 60 seconds before the token exires!

If you did not make this request, just simply ignore it and no changes will be made!
"""
    # 特地拉一條thread跟主程式支開來專門執行寄送emial，效率快很多，因為寄送也會需要current_app
    thr = Thread(target=send_reset_email, args=[msg]) 
    thr.start()
    return thr
    
def send_reset_email(msg):
    with current_app.app_context():
        mail.send(msg) # 寄出郵件