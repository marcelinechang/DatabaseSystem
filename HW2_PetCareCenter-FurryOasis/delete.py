from flask import Blueprint, request, redirect, url_for
import mysql.connector

delete_bp = Blueprint('delete_bp', __name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2024database',
    'database': 'test_db'
}

#delete_customer
@delete_bp.route('/delete_customer', methods=['POST'])
def delete_customer():
    selected_ids = request.form.getlist('customer_ids')
    
    if selected_ids:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        tables = [('customer', 'customer_id'), 
                  ('pet', 'owner_id'), 
                  ('appointment', 'owner_id')]

        for table, column in tables:
            delete_query = f"DELETE FROM {table} WHERE {column} IN (%s)" % ','.join(['%s'] * len(selected_ids))
            cursor.execute(delete_query, tuple(selected_ids))

        conn.commit()
        cursor.close()
        conn.close()
    
    return redirect(url_for('read_bp.index'))

#delete_pet
@delete_bp.route('/delete_pet', methods=['POST'])
def delete_pet():
    selected_ids = request.form.getlist('pet_ids')
    
    if selected_ids:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        tables = [('pet', 'pet_id'), 
                  ('appointment', 'pet_id')]

        for table, column in tables:
            delete_query = f"DELETE FROM {table} WHERE {column} IN (%s)" % ','.join(['%s'] * len(selected_ids))
            cursor.execute(delete_query, tuple(selected_ids))

        conn.commit()
        cursor.close()
        conn.close()
    
    return redirect(url_for('read_bp.index'))

#delete_appointment
@delete_bp.route('/delete_appointment', methods=['POST'])
def delete_appointment():
    selected_ids = request.form.getlist('appointment_ids')
    
    if selected_ids:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        delete_query = "DELETE FROM appointment WHERE appointment_id IN (%s)" % ','.join(['%s'] * len(selected_ids))
        cursor.execute(delete_query, tuple(selected_ids))

        conn.commit()
        cursor.close()
        conn.close()
    
    return redirect(url_for('read_bp.index'))

#delete_service
@delete_bp.route('/delete_service', methods=['POST'])
def delete_service():
    selected_ids = request.form.getlist('service_ids')
    
    if selected_ids:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        delete_query = "DELETE FROM service WHERE service_id IN (%s)" % ','.join(['%s'] * len(selected_ids))
        cursor.execute(delete_query, tuple(selected_ids))

        conn.commit()
        cursor.close()
        conn.close()
    
    return redirect(url_for('read_bp.index'))
