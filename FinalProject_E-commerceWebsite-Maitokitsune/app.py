from flask import Flask, render_template
from flask_login import LoginManager
from blueprints.auth import auth_bp
from blueprints.product import product_bp
from blueprints.cart import cart_bp
from blueprints.admin import admin_bp
from database import init_db
# from blueprints.order import order_bp

app = Flask(__name__)
app.config.from_object('config')
 
UPLOAD_FOLDER = 'static/'  # 照片存放的目錄
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 初始化登入管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# 註冊藍圖
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)

# 初始化資料庫
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.get_by_id(user_id)

if __name__ == '__main__':
    app.run(debug=True)
