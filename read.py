from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from create import create_bp

app = Flask(__name__)
app.register_blueprint(create_bp)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2024database',
    'database': 'test_db'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        # get [nickname] and [zodiac_sign] from user input
        nickname = request.form['nickname']
        zodiac_sign = request.form['zodiac']

        # insert into database
        insert_query = "INSERT INTO zodiac (nickname, zodiac_sign) VALUES (%s, %s)"
        cursor.execute(insert_query, (nickname, zodiac_sign))
        conn.commit()

        # redirect to index page
        return redirect(url_for('index'))

    # select all the data from zodiac table and present it on the website
    cursor.execute("SELECT * FROM zodiac")
    tables = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', tables=tables)

if __name__ == '__main__':
    app.run(debug=True)
