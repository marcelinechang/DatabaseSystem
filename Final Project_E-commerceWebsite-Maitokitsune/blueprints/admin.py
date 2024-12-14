from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import mysql.connector
from config import DB_CONFIG
from models.admin import Admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

'''登入管理'''
@admin_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 檢查管理員是否已存在
            cursor.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
            existing_admin = cursor.fetchone()
            
            if existing_admin:
                flash('User 已存在','danger')
                return redirect(url_for('admin.register'))
            
            # 插入新管理員
            cursor.execute(
                "INSERT INTO admin_users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            conn.commit()
            
            flash('註冊成功，請登入','success')
            return redirect(url_for('admin.login'))
        
        except mysql.connector.Error as err:
            flash(f'發生錯誤: {err}','danger')
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    return render_template('admin/register.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 驗證管理員
            cursor.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
            admin = cursor.fetchone()
            
            if admin and check_password_hash(admin['password'], password):
                admin_obj = Admin(id=admin['id'], username=admin['username'])
                login_user(admin_obj)
                flash('登入成功','success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('無效的使用者名稱或密碼','danger')
        
        except mysql.connector.Error as err:
            flash(f'發生錯誤: {err}','danger')
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出','success')
    return redirect(url_for('admin.login'))


'''Daschboard'''
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """
    管理後台首頁，包含銷售最佳產品的長條圖。
    """
    return render_template('admin/dashboard.html')

@admin_bp.route('/top-products')
def top_products():
    """
    API Endpoint: 返回前五名產品的銷售數據。
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.name, oi.flavor, oi.size, SUM(quantity) AS total_quantity
            FROM order_items oi
            LEFT JOIN products p
            ON oi.product_id = p.id
            GROUP BY p.name, oi.flavor, oi.size
            ORDER BY total_quantity DESC
            LIMIT 5;
            """)
        results = cursor.fetchall()

        data = [{
            "product_name": row["name"],
            "flavor": row["flavor"],
            "size": row["size"],
            "total_quantity": row["total_quantity"]
        } for row in results]
        return jsonify(data)

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
          
@admin_bp.route('/low-stock-products')
def low_stock_products():
    """
    API Endpoint: 返回庫存量小於等於 5 的產品資料。
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.name AS product_name, pv.flavor, pv.size, pv.stock
            FROM shop.product_variants pv
            LEFT JOIN products p
            ON pv.product_id = p.id
            WHERE pv.stock <= 5;
        """)
        results = cursor.fetchall()

        data = [{"product_name": row["product_name"],
                 "flavor": row["flavor"],
                 "size": row["size"],
                 "stock": row["stock"]} for row in results]
        return jsonify(data)

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


'''訂單管理'''
@admin_bp.route('/pending-orders', methods=['GET'])
@login_required
def pending_orders():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 查詢使用者的訂單
        cursor.execute('''
                       SELECT o.*, 
                       CONCAT(u.firstname,' ',u.lastname) AS username
                       FROM orders o
                       LEFT JOIN users u
                       ON o.user_id = u.id
                       WHERE status not in ('Completed', 'Cancelled') 
                       ORDER BY created_at
                       ''')
        orders = cursor.fetchall()
        
        return render_template('admin/pending_orders.html', orders=orders)
    
    except mysql.connector.Error as err:
        flash(f'發生錯誤: {err}','danger')
        return redirect(url_for('home'))
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@admin_bp.route('/completed-orders', methods=['GET'])
@login_required
def completed_orders():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 查詢使用者的訂單
        cursor.execute('''
                       SELECT o.*, 
                       CONCAT(u.firstname,' ',u.lastname) AS username
                       FROM orders o
                       LEFT JOIN users u
                       ON o.user_id = u.id
                       WHERE status ='Completed'
                       ORDER BY created_at DESC
                       ''')
        orders = cursor.fetchall()
        
        return render_template('admin/completed_orders.html', orders=orders)
    
    except mysql.connector.Error as err:
        flash(f'發生錯誤: {err}','danger')
        return redirect(url_for('home'))
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@admin_bp.route('/orders/<int:order_id>/details', methods=['GET'])
@login_required
def order_details(order_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 查詢訂單項目
        cursor.execute("""
            SELECT oi.quantity, oi.price, p.name, oi.flavor, oi.size 
            FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """, (order_id,))
        
        order_items = cursor.fetchall()

        # 將訂單項目傳回前端，這邊不需要額外模板，直接返回 JSON
        return jsonify(order_items)
    
    except mysql.connector.Error as err:
        flash(f'發生錯誤: {err}','danger')
        return redirect(url_for('home'))
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@admin_bp.route('/orders/<int:order_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # 查詢該訂單的詳細資料
        if request.method == 'GET':
            cursor.execute('''
                       SELECT o.*, 
                       CONCAT(u.firstname,' ',u.lastname) AS username
                       FROM orders o
                       LEFT JOIN users u
                       ON o.user_id = u.id
                       WHERE o.id = %s
                       ''', (order_id,))
            order = cursor.fetchone()
            
            if not order:
                flash('訂單不存在','danger')
                return redirect(url_for('admin.pending_orders'))

            return render_template('admin/edit_order.html', order=order)

        # 修改訂單資料
        if request.method == 'POST':
            status = request.form['status']
            cursor.execute(
                "UPDATE orders SET status = %s WHERE id = %s",
                (status, order_id)
            )
            conn.commit()
            flash('訂單已更新','success')
            return redirect(url_for('admin.pending_orders'))

    except mysql.connector.Error as err:
        flash(f'發生錯誤: {err}','danger')
        return redirect(url_for('admin.pending_orders'))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@admin_bp.route('/orders/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 取得該訂單中所有的商品及數量
        cursor.execute('''SELECT pv.id as variant_id, oi.quantity 
                       FROM order_items oi
                       LEFT JOIN product_variants pv
                       ON oi.flavor = pv.flavor and oi.size = pv.size
                       WHERE order_id = %s''', (order_id,))
        order_items = cursor.fetchall()

        # 將每個商品的數量加回到 products 表中的庫存
        for variant_id, quantity in order_items:
            cursor.execute(
                "UPDATE product_variants SET stock = stock + %s WHERE id = %s", 
                (quantity, variant_id)
            )

        # 刪除訂單相關的項目及訂單
        # cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        conn.commit()

        return jsonify({'success': True, 'message': '訂單已刪除，庫存已更新'})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'刪除失敗: {err}'})

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


'''商品管理'''
UPLOAD_FOLDER = 'static/'  # 照片存放的目錄
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        # 接收商品主要資訊
        name = request.form.get('name')
        description = request.form.get('description')
        image_file = request.files.get('image')

        # 接收多個口味、尺寸、價格與庫存
        flavors = request.form.getlist('flavor')
        sizes = request.form.getlist('size')
        prices = request.form.getlist('price')
        stocks = request.form.getlist('stock')

        # 驗證必填欄位
        if not name or not description:
            flash('商品名稱和描述為必填項目！', 'danger')
            return redirect(url_for('admin.add_product'))

        # 驗證選項資料的完整性
        if not (flavors and sizes and prices and stocks) or \
                not (len(flavors) == len(sizes) == len(prices) == len(stocks)):
            flash('請完整填寫所有商品資訊！', 'danger')
            return redirect(url_for('admin.add_product'))

        # 處理照片上傳
        filename = None
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        elif image_file:
            flash('不支援的檔案格式！', 'danger')
            return redirect(url_for('admin.add_product'))

        # 儲存商品資料到資料庫
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # 插入商品主表資料
            cursor.execute(
                """
                INSERT INTO products (name, description, image_url)
                VALUES (%s, %s, %s)
                """,
                (name, description, image_path)
            )
            product_id = cursor.lastrowid

            # 插入商品選項資料
            for flavor, size, price, stock in zip(flavors, sizes, prices, stocks):
                cursor.execute(
                    """
                    INSERT INTO product_variants (product_id, flavor, size, price, stock)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (product_id, flavor, size, price, stock)
                )

            conn.commit()
            flash('商品新增成功！', 'success')
            return redirect(url_for('admin.view_product'))
        except Exception as e:
            flash(f'商品新增失敗: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('admin/add_product.html')



@admin_bp.route('/product')
@login_required
def view_product():
    """查看庫存"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''SELECT * FROM products''')
        items = cursor.fetchall()
        return render_template('admin/product.html', items=items)
    
    except mysql.connector.Error as err:
        flash(f'發生錯誤: {err}','danger')
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """修改商品與其所有選項"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            # 更新商品基本資訊
            name = request.form.get('name')
            description = request.form.get('description')
            image_file = request.files.get('image')

            if not name or not description:
                flash('商品名稱和描述為必填項目！', 'danger')
                return redirect(url_for('admin.edit_product', product_id=product_id))

            filename = None
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                cursor.execute(
                    """
                    UPDATE products SET name = %s, description = %s, image_url = %s WHERE id = %s
                    """,
                    (name, description, image_path, product_id)
                )
            else:
                cursor.execute(
                    """
                    UPDATE products SET name = %s, description = %s WHERE id = %s
                    """,
                    (name, description, product_id)
                )

            # 更新商品選項
            variants = request.form.getlist('variant_id')
            flavors = request.form.getlist('flavor')
            sizes = request.form.getlist('size')
            prices = request.form.getlist('price')
            stocks = request.form.getlist('stock')

            for i in range(len(variants)):
                cursor.execute(
                    """
                    UPDATE product_variants SET flavor = %s, size = %s, price = %s, stock = %s WHERE id = %s
                    """,
                    (flavors[i], sizes[i], prices[i], stocks[i], variants[i])
                )

            conn.commit()
            flash('商品已成功更新！', 'success')
            return redirect(url_for('admin.view_product'))

        # 獲取商品與選項資料
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            flash(f'找不到編號為 {product_id} 的商品', 'danger')
            return redirect(url_for('admin.view_product'))

        cursor.execute("SELECT * FROM product_variants WHERE product_id = %s", (product_id,))
        variants = cursor.fetchall()

        return render_template('admin/edit_product.html', product=product, variants=variants)

    except mysql.connector.Error as err:
        flash(f'發生錯誤: {err}', 'danger')
        return redirect(url_for('admin.view_product'))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    """刪除商品"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 刪除商品及其所有選項
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()

        return jsonify({"success": True, "message": "商品已成功刪除！"})
    except mysql.connector.Error as err:
        return jsonify({"success": False, "message": f"刪除商品時發生錯誤: {err}"})
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
