from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import DB_CONFIG
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        
        # 密碼雜湊
        hashed_password = generate_password_hash(password)
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 檢查使用者是否已存在
            cursor.execute("SELECT * FROM users WHERE email = %s OR phone = %s", 
                           (email, phone))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('phone或email已存在','danger')
                return redirect(url_for('auth.register'))
            
            # 插入新使用者
            cursor.execute(
                "INSERT INTO users (firstname, lastname, email, password, phone, address) VALUES (%s, %s, %s, %s, %s, %s)",
                (firstname, lastname, email, hashed_password, phone, address)
            )
            conn.commit()
            
            flash('註冊成功，請登入','success')
            return redirect(url_for('auth.login'))
        
        except mysql.connector.Error as err:
            flash(f'發生錯誤: {err}','danger')
            return redirect(url_for('auth.register'))
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 驗證使用者
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                # 創建使用者物件
                user_obj = User(
                    id=user['id'], 
                    email=user['email']
                )
                login_user(user_obj)
                flash('登入成功','success')
                return redirect(url_for('product.list_products'))
            else:
                flash('無效的使用者名稱或密碼','danger')
        
        except mysql.connector.Error as err:
            flash(f'發生錯誤: {err}','danger')
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出','success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    """
    顯示會員資料
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 獲取當前用戶資料
        cursor.execute("SELECT firstname, lastname, email, phone, address FROM users WHERE id = %s", 
                       (current_user.id,))
        user_info = cursor.fetchone()
        
        return render_template('profile.html', user_info=user_info)
    
    except mysql.connector.Error as err:
        flash(f'無法加載會員資料: {err}','danger')
        return redirect(url_for('product.list_products'))
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@auth_bp.route('/orders', methods=['GET'])
@login_required
def orders():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 查詢使用者的訂單
        cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC", (current_user.id,))
        orders = cursor.fetchall()
        
        return render_template('orders.html', orders=orders)
    
    except mysql.connector.Error as err:
        flash(f'發生錯誤: {err}','danger')
        return redirect(url_for('home'))
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@auth_bp.route('/orders/<int:order_id>/details', methods=['GET'])
@login_required
def order_details(order_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 查詢訂單項目
        cursor.execute("""
            SELECT oi.quantity, oi.price, p.name, oi.flavor, oi.size 
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
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
        
@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            # 取得表單資料
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']

            # 更新會員資料
            cursor.execute("""
                UPDATE users 
                SET firstname = %s, lastname = %s, email = %s, phone = %s, address = %s 
                WHERE id = %s
            """, (firstname, lastname, email, phone, address, current_user.id))
            conn.commit()

            flash('資料更新成功！', 'success')
            return redirect(url_for('auth.profile'))  # 重定向回會員資料頁面

        # 取得用戶資料
        cursor.execute("SELECT * FROM users WHERE id = %s", (current_user.id,))
        user_info = cursor.fetchone()

        return render_template('edit_profile.html', user_info=user_info)

    except mysql.connector.Error as err:
        flash(f'發生錯誤: {err}', 'danger')
        return redirect(url_for('home'))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()