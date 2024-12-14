from flask_login import UserMixin
import mysql.connector
from config import DB_CONFIG

class Admin(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username
    
    @staticmethod
    def get_by_id(admin_id):
        """根據ID獲取管理員"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM admin_users WHERE id = %s", (admin_id,))
            admin = cursor.fetchone()
            
            if admin:
                return Admin(
                    id=admin['id'], 
                    username=admin['username']
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
        return True