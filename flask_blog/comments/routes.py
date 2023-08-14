from flask import Blueprint, redirect, request, url_for, render_template, flash
from flask_login import  current_user, login_required
from flask_blog.models import Comment, Like, Post
from flask_blog import db
import re
from datetime import datetime

comments = Blueprint('comments', __name__)


@comments.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    if not content:
        flash('留言不得為空', category='danger')
        return redirect(url_for('posts.post', post_id=post_id))
    print(post.id, content)
    striped_tag_content = re.sub(r'<[^>]+>','',content)
    comment = Comment(content = striped_tag_content, user_id = current_user.id, post_id = post_id)
    db.session.add(comment)
    db.session.commit()
    flash(f'使用者{current_user.username}已成功新增留言!', category='success')
    return redirect(url_for('posts.post', post_id=post_id))

@comments.route('/comment/<int:comment_id>/thumb_toggle', methods=['POST'])
@login_required
def thumb_toggle(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    toggle = request.get_json()
    print(toggle)
    if toggle['change'] == 1:
        like_comment = Like(user_id=current_user.id, comment_id=comment.id)
        db.session.add(like_comment)
        db.session.commit()
    else:
        Like.query.filter_by(comment_id=comment.id, user_id=current_user.id).delete()
        db.session.commit()
        
    return {'data':(current_user.username, comment.id)}

@comments.route('/reply/<int:post_id>/<int:comment_id>', methods=['POST'])
@login_required
def reply(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    content = request.get_json()['content']
    striped_tag_content = re.sub(r'<[^>]+>','',content) # 前端其實已經做過了 這行可放可不放
    print(content)
    reply = Comment(content=striped_tag_content, user_id=current_user.id, post_id=post_id, reply_id=comment_id)
    db.session.add(reply)
    db.session.commit()
    partial_template = render_template('reply_template.html', post=post, comment=reply)
    
    return {'data':partial_template}

@comments.route('/edit/comment/<int:post_id>/<int:comment_id>', methods=['POST'])
def edit_comment(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    new_content = request.form.get('new_content')
    comment.content = new_content
    comment.date_edited = datetime.utcnow()
    db.session.commit()
    flash('留言更新成功', category='success')
    return redirect(url_for('posts.post', post_id=post_id))

@comments.route('/comment/<int:post_id>/cancel_edit', methods=['POST'])
def cancel_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return redirect(url_for('posts.post', post_id=post_id))

@comments.route('/delete/comment/<int:post_id>/<int:comment_id>', methods=['POST'])
def delete_comment(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    comment.delete = 1
    comment.date_deleted = datetime.utcnow()
    db.session.commit()
    flash('留言刪除成功', category='success')
    return redirect(url_for('posts.post', post_id=post_id))