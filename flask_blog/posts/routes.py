from flask import Blueprint
from flask import render_template, request, url_for, flash, redirect, abort
from flask_blog.posts.forms import PostForm
from flask_blog.models import Post
from flask_blog import db
from flask_login import  current_user, login_required
from datetime import datetime

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm() # 空白表單
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=form)

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id) # 找的到就傳id找不到就直接跳404頁面
    return render_template('post.html', title=post.title, post=post)

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
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form)

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