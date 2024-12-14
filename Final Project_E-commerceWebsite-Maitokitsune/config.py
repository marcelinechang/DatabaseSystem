import os

# 安全密鑰，用於session和CSRF保護
SECRET_KEY = os.urandom(24)

# 資料庫連線設定
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2024database',
    'database': 'shop'
}

# 其他配置
DEBUG = True
