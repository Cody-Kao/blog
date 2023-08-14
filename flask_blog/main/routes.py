from flask import Blueprint, request, render_template, abort
from flask_blog.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int) # 製造一個optional的參數:頁數， 1是預設值， 並且只接受int
    # 先把所有貼文依照貼文時間做由新到舊排序，再把他們分成若干頁，一頁只有X則(per_page)，目前在第page頁
    category = request.args.get('category', None) #如果沒有指定要哪個category，則顯示全部貼文
    if not category:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    elif category in {'Travel', 'Food', 'Style'}:
        print(f'yes the category is: {category}')
        posts = Post.query.filter_by(category=category).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    else:
        abort(404)
    return render_template('home.html', title = 'Home', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title = 'about')