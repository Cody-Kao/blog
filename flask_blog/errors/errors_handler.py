from flask import Blueprint, render_template

# 新增一個專門處理錯誤的blueprint

errors = Blueprint('errors', __name__) # 創造另一個blueprint

# 這裡用app_errorhandler而不是errorhandler是因為，前者可以支援整份檔案，而後者僅限此blueprint
@errors.app_errorhandler(404) 
def error_404(error): # 記得把error參數加入
    return render_template('errors/404.html'), 404 # flask預設第二個參數為200，所以要記得改成404

@errors.app_errorhandler(403) 
def error_403(error): 
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500) 
def error_500(error):
    return render_template('errors/500.html'), 500