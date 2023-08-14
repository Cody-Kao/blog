from flask import Blueprint
from flask import render_template, request, url_for, flash, redirect, abort, send_from_directory, current_app
from flask_blog.posts.forms import PostForm
from flask_blog.models import Post, Comment
from flask_blog import db
from flask_login import  current_user, login_required
from datetime import datetime
from flask_ckeditor import upload_success, upload_fail
import os

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm() # 空白表單
    if form.validate_on_submit():
        post = Post(title=form.title.data, category=form.category.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=form)

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id) # 找的到就傳id找不到就直接跳404頁面
    comments = Comment.query.filter_by(post_id=post_id, reply_id=None).all()
    if current_user.get_id(): # 只有在不是anynomoususer的情況下才會有likes的屬性，然後取得所有這個使用者按讚的留言並傳入template
        liked_comments_id = [liked_comment.comment_id for liked_comment in current_user.likes]
        print('permitted user')
    else:
        liked_comments_id = []
    print('liked_comments_id: ', liked_comments_id)
    if current_user.get_id() and current_user.id != post.author.id: # 確保如果是未登入使用者(AnonymousUser)存取不會報錯，而是把id設成None
        views = post.view
        post.view = views + 1
        db.session.commit()
    return render_template('post.html', title=post.title, post=post, comments=comments, liked_comments_id=liked_comments_id)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.username != current_user.username: # 檢查是否為同個使用者po的文章， 是才能編輯， 否則導入forbidden介面
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_edited = datetime.utcnow()
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id)) 
    elif request.method == 'GET': # 在一開始進來時，將空白表單先複寫為資料庫內的資料
        form.title.data = post.title
        form.category.data = post.category
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form, post=post)

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.username != current_user.username:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been DELETED', 'success')
    return redirect(url_for('main.home'))

@posts.route('/files/<path:filename>')
def uploaded_files(filename):
    path = os.path.join(current_app.root_path, 'static', 'upload_pics')
    return send_from_directory(path, filename)

@posts.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    file_type = f.filename.split('.')[-1].lower()
    if file_type not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(current_app.root_path, 'static', 'upload_pics', f.filename))
    url = url_for('posts.uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)  # return upload_success call