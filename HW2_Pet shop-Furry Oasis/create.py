from flask import Blueprint, request, redirect, url_for
import mysql.connector

create_bp = Blueprint('create_bp', __name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2024database',
    'database': 'test_db'
}

@create_bp.route('/new_add_appointment', methods=['POST'])
def new_add_appointment():

    # Establish database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    #customer
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    birthday = request.form['birthday']
    phone = request.form['phone']
    email = request.form['email']

    #pet
    owner_phone = request.form['owner_phone']
    pet_name = request.form['pet_name']
    sex = request.form['sex']
    birth_year = request.form['birth_year']
    height = request.form['height']
    weight = request.form['weight']

    if request.form['species'] == 'other':
        species = request.form['other_species']
    else:
        species = request.form['species']
    
    #appointment
    appointment_date = request.form['appointment_date']
    appointment_time = request.form['appointment_time']
    appointment_type = request.form['appointment_type']

    if first_name != '':

        insert_query = """INSERT INTO customer (first_name, last_name, birthday, phone, email) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (first_name, last_name, birthday, phone, email))
        conn.commit()

        # owner_id
        ownerid_query = """SELECT MAX(customer_id) FROM customer"""
        cursor.execute(ownerid_query)
        get_ownerid = cursor.fetchone()
        owner_id = get_ownerid[0]

        insert_query = """INSERT INTO pet (pet_name, owner_id, sex, species, birth_year, height, weight) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (pet_name, owner_id, sex, species, birth_year, height, weight))
        conn.commit()

        # pet_id
        petid_query = """SELECT MAX(pet_id) FROM pet"""
        cursor.execute(petid_query)
        get_petid = cursor.fetchone()
        pet_id = get_petid[0]

        # purpose
        serviceid_query = """SELECT service_id FROM service WHERE service_name = %s"""
        cursor.execute(serviceid_query,(appointment_type,))
        get_serviceid = cursor.fetchone()
        service_id = get_serviceid[0]

        insert_query = """INSERT INTO appointment (pet_id, owner_id, appointment_date, appointment_time, purpose) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (pet_id, owner_id, appointment_date, appointment_time, service_id))
        conn.commit()

    else:
        # owner_id
        ownerid_query = """SELECT customer_id FROM customer WHERE phone = %s"""
        cursor.execute(ownerid_query, (owner_phone,))
        get_ownerid = cursor.fetchone()
        owner_id = get_ownerid[0]

        insert_query = """INSERT INTO pet (pet_name, owner_id, sex, species, birth_year, height, weight) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (pet_name, owner_id, sex, species, birth_year, height, weight))
        conn.commit()

        # pet_id
        petid_query = """SELECT MAX(pet_id) FROM pet"""
        cursor.execute(petid_query)
        get_petid = cursor.fetchone()
        pet_id = get_petid[0]

        # purpose
        serviceid_query = """SELECT service_id FROM service WHERE service_name = %s"""
        cursor.execute(serviceid_query,(appointment_type,))
        get_serviceid = cursor.fetchone()
        service_id = get_serviceid[0]

        insert_query = """INSERT INTO appointment (pet_id, owner_id, appointment_date, appointment_time, purpose) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (pet_id, owner_id, appointment_date, appointment_time, service_id))
        conn.commit()
    

    # Close the database connection
    cursor.close()
    conn.close()
        
    # Redirect to another page after successful submission
    return redirect(url_for('read_bp.index'))

@create_bp.route('/existed_add_appointment', methods=['POST'])
def existed_add_appointment():

    # Establish database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    #pet
    owner_phone = request.form['owner_phone']
    pet_name = request.form['pet_name']
    
    #appointment
    appointment_date = request.form['appointment_date']
    appointment_time = request.form['appointment_time']
    appointment_type = request.form['appointment_type']

    # owner_id
    ownerid_query = """SELECT customer_id FROM customer WHERE phone = %s"""
    cursor.execute(ownerid_query, (owner_phone,))
    get_ownerid = cursor.fetchone()
    owner_id = get_ownerid[0]

    # pet_id
    petid_query = """SELECT pet_id FROM pet WHERE owner_id = %s AND pet_name = %s"""
    cursor.execute(petid_query, (owner_id, pet_name))
    get_petid = cursor.fetchone()
    pet_id = get_petid[0]

    # purpose
    serviceid_query = """SELECT service_id FROM service WHERE service_name = %s"""
    cursor.execute(serviceid_query,(appointment_type,))
    get_serviceid = cursor.fetchone()
    service_id = get_serviceid[0]

    insert_query = """INSERT INTO appointment (pet_id, owner_id, appointment_date, appointment_time, purpose) VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(insert_query, (pet_id, owner_id, appointment_date, appointment_time, service_id))
    conn.commit()
    

    # Close the database connection
    cursor.close()
    conn.close()
        
    # Redirect to another page after successful submission
    return redirect(url_for('read_bp.index'))

@create_bp.route('/add_service', methods=['POST'])
def add_service():
    # Process the Add Services form
    service_name = request.form['service_name']
    service_type = request.form['service_type']
    description = request.form['description']
    price = request.form['price']
    duration = request.form['duration']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    insert_query = """INSERT INTO service (service_name, service_type, description, price, duration_minutes)
                      VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(insert_query, (service_name, service_type, description, price, duration))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.index'))