from flask import Blueprint, render_template
import mysql.connector

read_bp = Blueprint('read_bp', __name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2024database',
    'database': 'test_db'
}

@read_bp.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # select all the data from zodiac table and present it on the website
    select_query = "SELECT * FROM zodiac"
    cursor.execute(select_query)
    posts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', posts=posts)
