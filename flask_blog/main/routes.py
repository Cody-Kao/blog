from flask import Blueprint, request, render_template
from flask_blog.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int) # 製造一個optional的參數:頁數， 1是預設值， 並且只接受int
    # 先把所有貼文依照貼文時間做由新到舊排序，再把他們分成若干頁，一頁只有一則(per_pageㄥ)，目前在第page頁
    posts = Post.query.order_by(Post.date_edited.desc()).paginate(page=page, per_page=1)
    return render_template('home.html', title = 'Home', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title = 'about')