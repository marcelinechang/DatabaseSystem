from flask import Blueprint, request, redirect, url_for
import mysql.connector

create_bp = Blueprint('create_bp', __name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2024database',
    'database': 'test_db'
}

@create_bp.route('/add', methods=['POST'])
def add_post():

    nickname = request.form['nickname']
    zodiac_sign = request.form['zodiac']
        
    # Establish database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
        
    # Insert the nickname and zodiac sign into the zodiac table
    insert_query = "INSERT INTO zodiac (nickname, zodiac_sign) VALUES (%s, %s)"
    cursor.execute(insert_query, (nickname, zodiac_sign))
    conn.commit()
        
    # Close the database connection
    cursor.close()
    conn.close()
        
    # Redirect to another page after successful submission
    return redirect(url_for('read_bp.index'))
