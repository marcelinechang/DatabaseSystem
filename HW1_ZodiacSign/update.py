from flask import Blueprint, request, redirect, url_for
import mysql.connector

update_bp = Blueprint('update_bp', __name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2024database',
    'database': 'test_db'
}

@update_bp.route('/update/<int:post_id>', methods=['POST'])
def update_post(post_id):

    new_nickname = request.form.get(f'post_{post_id}')
    new_zodiac_sign = request.form.get(f'zodiac_sign_{post_id}')
    
    if not new_nickname:
        return "No content to update", 400  
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    update_query = "UPDATE zodiac SET nickname = %s, zodiac_sign = %s WHERE id = %s"
    
    cursor.execute(update_query, (new_nickname, new_zodiac_sign, post_id))
    conn.commit()  
    
    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.index'))