from flask_login import UserMixin
import mysql.connector
from config import DB_CONFIG

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email
    
    @staticmethod
    def get_by_id(user_id):
        """根據ID獲取使用者"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if user:
                return User(
                    id=user['id'], 
                    email=user['email']
                )
            return None
        
        except mysql.connector.Error:
            return None
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    @property
    def is_admin(self):
        return False
    
    