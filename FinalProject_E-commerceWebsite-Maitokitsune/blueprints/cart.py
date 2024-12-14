from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import mysql.connector
from config import DB_CONFIG

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # 獲取表單提交的數據
    flavor = request.form.get('flavor')  # 口味
    size = request.form.get('size')  # 容量
    quantity = request.form.get('quantity', 1, type=int)  # 數量

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # 確認該商品變體是否存在且庫存足夠
        cursor.execute("""
            SELECT stock 
            FROM product_variants
            WHERE product_id = %s AND flavor = %s AND size = %s
        """, (product_id, flavor, size))
        variant = cursor.fetchone()

        if not variant:
            flash('所選的商品選項不存在','danger')
            return redirect(url_for('product.list_products'))
        if variant['stock'] < quantity:
            flash('商品庫存不足','danger')
            return redirect(url_for('product.list_products'))

        # 檢查購物車是否已有此商品變體
        cursor.execute("""
            SELECT * 
            FROM cart 
            WHERE user_id = %s AND product_id = %s AND flavor = %s AND size = %s
        """, (current_user.id, product_id, flavor, size))
        existing_cart_item = cursor.fetchone()

        if existing_cart_item:
            # 更新購物車中的數量
            cursor.execute("""
                UPDATE cart 
                SET quantity = quantity + %s 
                WHERE user_id = %s AND product_id = %s AND flavor = %s AND size = %s
            """, (quantity, current_user.id, product_id, flavor, size))
        else:
            # 新增購物車項目
            cursor.execute("""
                INSERT INTO cart (user_id, product_id, flavor, size, quantity) 
                VALUES (%s, %s, %s, %s, %s)
            """, (current_user.id, product_id, flavor, size, quantity))

        conn.commit()
        flash('商品已成功加入購物車','success')
        return redirect(url_for('product.list_products'))

    except mysql.connector.Error as err:
        flash(f'加入購物車時發生錯誤: {err}','danger')
        return redirect(url_for('product.list_products'))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@cart_bp.route('/cart')
@login_required
def view_cart():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # 獲取使用者購物車內容，包括口味和容量
        cursor.execute("""
            SELECT c.id, p.name, c.flavor, c.size, c.quantity, v.price, (v.price * c.quantity) as total 
            FROM cart c 
            JOIN products p ON c.product_id = p.id 
            JOIN product_variants v ON v.product_id = c.product_id 
                AND v.flavor = c.flavor 
                AND v.size = c.size
            WHERE c.user_id = %s
        """, (current_user.id,))
        cart_items = cursor.fetchall()

        # 計算總金額
        total_price = sum(item['total'] for item in cart_items)

        return render_template('cart.html', cart_items=cart_items, total_price=total_price)

    except mysql.connector.Error as err:
        flash(f'載入購物車時發生錯誤: {err}','danger')
        return redirect(url_for('product.list_products'))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@cart_bp.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 找出要刪除的購物車項目
        cursor.execute(
            "SELECT * FROM cart WHERE id = %s AND user_id = %s", 
            (cart_item_id, current_user.id)
        )
        cart_item = cursor.fetchone()
        
        if cart_item:
            # 刪除購物車項目並退回庫存
            cursor.execute(
                "DELETE FROM cart WHERE id = %s", 
                (cart_item_id,)
            )
            conn.commit()
            flash('商品已從購物車移除','success')
        else:
            flash('無效的購物車項目','danger')
        
        return redirect(url_for('cart.view_cart'))
    
    except mysql.connector.Error as err:
        flash(f'移除購物車項目時發生錯誤: {err}','danger')
        return redirect(url_for('cart.view_cart'))
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 獲取購物車內容
        cursor.execute("""
            SELECT c.product_id, c.flavor, c.size, c.quantity, v.price, (c.quantity * v.price) as total
            FROM cart c
            JOIN product_variants v ON c.product_id = v.product_id
                AND c.flavor = v.flavor
                AND c.size = v.size
            WHERE c.user_id = %s
        """, (current_user.id,))
        cart_items = cursor.fetchall()

        if not cart_items:
            flash('購物車是空的，無法送出訂單','danger')
            return redirect(url_for('cart.view_cart'))
        
        # 計算總金額
        total_price = sum(item['total'] for item in cart_items)
        
        # 建立訂單
        cursor.execute("""
            INSERT INTO orders (user_id, total_price, status) 
            VALUES (%s, %s, %s)
        """, (current_user.id, total_price, 'Pending'))
        order_id = cursor.lastrowid
        
        # 將購物車內容寫入訂單明細，並減少庫存
        for item in cart_items:
            # 插入訂單明細
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, flavor, size, quantity, price) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (order_id, item['product_id'], item['flavor'], item['size'], item['quantity'], item['price']))
            
            # 更新庫存
            cursor.execute("""
                UPDATE product_variants 
                SET stock = stock - %s 
                WHERE product_id = %s AND flavor = %s AND size = %s
            """, (item['quantity'], item['product_id'], item['flavor'], item['size']))
        
        # 清空購物車
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (current_user.id,))
    
        conn.commit()
        
        # 跳轉到訂單成功頁面
        return redirect(url_for('cart.order_success', order_id=order_id))
    
    except mysql.connector.Error as err:
        flash(f'送出訂單時發生錯誤: {err}','danger')
        return redirect(url_for('cart.view_cart'))
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@cart_bp.route('/order_success/<int:order_id>')
@login_required
def order_success(order_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 獲取訂單資訊
        cursor.execute("""
            SELECT o.id, o.total_price, o.status, o.created_at
            FROM orders o
            WHERE o.id = %s AND o.user_id = %s
        """, (order_id, current_user.id))
        order = cursor.fetchone()
        
        if not order:
            flash('找不到相關訂單','danger')
            return redirect(url_for('cart.view_cart'))
        
        return render_template('order_success.html', order=order)
    
    except mysql.connector.Error as err:
        flash(f'載入訂單時發生錯誤: {err}','danger')
        return redirect(url_for('cart.view_cart'))
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
