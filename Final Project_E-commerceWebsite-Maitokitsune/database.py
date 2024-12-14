import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    """建立資料庫連線"""
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """初始化資料庫表格"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 創建使用者表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        firstname VARCHAR(50) UNIQUE NOT NULL,
        lastname VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(10) UNIQUE NOT NULL,
        address VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_at TIMESTAMP
    )""")
    
    # 創建商品表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        image_url VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # 創建商品細節表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_variants (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT NOT NULL,
        flavor VARCHAR(50) NOT NULL,
        size VARCHAR(50) NOT NULL,
        price DECIMAL(4, 0) NOT NULL,
        stock INT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    )""")
    
    # 創建購物車表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        flavor VARCHAR(50) NOT NULL,
        size VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )""")

    
    # 創建訂單表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,         
        user_id INT NOT NULL,                      
        total_price DECIMAL(10, 2) NOT NULL,       
        status ENUM('Pending', 'Paid', 'Shipped', 'Completed', 'Cancelled') DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE 
    )""")
    
    # 創建訂單表格
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,         
        order_id INT NOT NULL,                     
        product_id INT NOT NULL,  
        flavor VARCHAR(50) NOT NULL,
        size VARCHAR(50) NOT NULL,                 
        quantity INT NOT NULL,                     
        price DECIMAL(10, 2) NOT NULL,             
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE, 
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE 
    )""")
    
     # 創建管理者名單
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP
    )""")
    
    
    
    
    conn.commit()
    cursor.close()
    conn.close()

def close_db_connection(conn):
    """關閉資料庫連線"""
    if conn:
        conn.close()

if __name__ == "__main__":
    init_db()
    print("資料庫初始化成功!")
