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

    # Fetch data for each table
    upcoming_query =  """
    SELECT 
        appointment_id, 
        pet_name, 
        species, 
        CONCAT(first_name, ' ', last_name) AS owner_name, 
        phone, 
        appointment_date AS date, 
        appointment_time AS time, 
        service_name AS service
    FROM 
        appointment
    LEFT JOIN 
        pet ON appointment.pet_id = pet.pet_id
    LEFT JOIN 
        customer ON appointment.owner_id = customer.customer_id
    LEFT JOIN 
    service ON appointment.purpose = service.service_id
    WHERE 
        appointment_date BETWEEN CURDATE() AND CURDATE() + 7
    ORDER BY 
        appointment_date, appointment_time
"""
    cursor.execute(upcoming_query)
    upcoming_appointments = cursor.fetchall()

    # customer info
    customer_query = """SELECT * FROM customer"""  # Add your query for upcoming appointments
    cursor.execute(customer_query)
    customer_info = cursor.fetchall()
    
    # pet info
    pet_query = """SELECT * FROM pet"""  # Add your query for completed appointments
    cursor.execute(pet_query)
    pet_info = cursor.fetchall()
    
    #appointment info
    appointment_query = """
    SELECT * 
    FROM appointment
    ORDER BY appointment_date DESC, appointment_time ASC"""  # Add your query for cancelled appointments
    cursor.execute(appointment_query)
    appointment_info = cursor.fetchall()

    # service info
    service_query = """SELECT * FROM service"""  # Add your query for cancelled appointments
    cursor.execute(service_query)
    service_info = cursor.fetchall()

    # species
    species_query = """SELECT DISTINCT species FROM pet""" 
    cursor.execute(species_query)
    species_results = cursor.fetchall()
    species_options = [sp['species'] for sp in species_results]

    # service
    service_query = """SELECT service_name FROM service""" 
    cursor.execute(service_query)
    service_results = cursor.fetchall()
    service_options = [sp['service_name'] for sp in service_results]

    cursor.close()
    conn.close()

    return render_template('index.html', 
                           upcoming_appointments = upcoming_appointments, 
                           customer_info = customer_info,
                           pet_info = pet_info,
                           appointment_info = appointment_info,
                           service_info = service_info,
                           species_options = species_options,
                           service_options = service_options)
