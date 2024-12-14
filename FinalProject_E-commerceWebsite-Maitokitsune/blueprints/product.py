from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import mysql.connector
from config import DB_CONFIG

product_bp = Blueprint('product', __name__)

@product_bp.route('/products')
def list_products():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 獲取商品及其選項資料
        cursor.execute("""
            SELECT p.id AS product_id, p.name, p.description, p.image_url,
                v.id AS variant_id, v.flavor, v.size, v.stock, v.price
            FROM products p
            LEFT JOIN product_variants v ON p.id = v.product_id
        """)
        rows = cursor.fetchall()
        
        # 整理數據，按產品分類
        products = {}
        for row in rows:
            product_id = row["product_id"]
            if product_id not in products:
                products[product_id] = {
                    "id": row["product_id"],
                    "name": row["name"],
                    "description": row["description"],
                    "image_url": row["image_url"],
                    "variants": []
                }
            products[product_id]["variants"].append({
                "variant_id": row["variant_id"],
                "flavor": row["flavor"],
                "size": row["size"],
                "stock": row["stock"],
                "price":row["price"]
            })
        
        return render_template('products.html', products=products.values())
    
    except mysql.connector.Error as err:
        flash(f'載入商品時發生錯誤: {err}', 'danger')
        return redirect(url_for('home'))
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
