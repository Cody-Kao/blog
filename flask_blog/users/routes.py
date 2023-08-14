from flask import Blueprint
from flask import render_template, request, url_for, flash, redirect
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                              RequestResetForm, ResetPasswordForm)
from flask_blog.models import User, Post
from flask_blog import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from flask_blog.users.utils import save_picture, write_reset_email


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(['Successfully Create Account for', form.username.data], 'success') # 最後一個參數是category，讓bootstrap能夠吃到
        # flash message 可以讓下一個template吃到
        return redirect(url_for('users.login'))
    return render_template('register.html', title = 'Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # 檢查輸入的密碼
            login_user(user, remember=form.remember.data) # 這裡是傳user(一個class)進去，而不是user.id
            next_page = request.args.get('next') 
            # 如果在被叫到log in頁面之前有先進去其他網頁才被導入到這裡，則網址會有個next的參數，表示登陸後會自動導入到那裏
            # 所以這時候就要把使用者render到那個頁面，而非主頁(home)
            flash(f'{current_user.username} log in successfully!', category='success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Log In Unsuccessfully, Please Check Email or Password', 'danger')
    return render_template('login.html', title = 'Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET': # 預先把表格內容填充資料庫的資料
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # 產生一個url
    return render_template('account.html', title = 'Account', image_file=image_file, form=form)

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    # 找到指定的使用者
    user = User.query.filter_by(username=username).first_or_404()
    # 找出他所有的貼文
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('user_posts.html', title = f'User-{username}', posts=posts, user=user)

@users.route('/reset_password', methods=['GET', 'POST']) # 使用者申請更改密碼: 輸入電子郵件通過認證後會寄token到信箱
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        write_reset_email(user)
        flash('The email with instructions to reset your email has been sent!', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The token is invalid or expired! Please request again!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been UPDATED! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)