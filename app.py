from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",  # Replace with your MySQL host
        user="root",       # Replace with your MySQL username
        password="2024database", # Replace with your MySQL password
        database="sys"  # Replace with your database name
    )
    return connection

@app.route('/')
def index():
    # Fetch data from the sys_config table
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sys_config")
    sys_config = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    # Render the external HTML template
    return render_template('sys_table.html', sys_config=sys_config)

if __name__ == '__main__':
    app.run(debug=True)
