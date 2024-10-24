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
def update_customer(post_id):

    new_first_name = request.form.get(f'first_name_{post_id}')
    new_last_name = request.form.get(f'last_name_{post_id}')
    new_birthday = request.form.get(f'birthday_{post_id}')
    new_phone = request.form.get(f'phone_{post_id}')
    new_email = request.form.get(f'email_{post_id}')

    if not new_first_name and not new_last_name and not new_birthday and not new_phone and not new_email:
        return "No content to update", 400  
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    update_query = """
    UPDATE customer SET first_name = %s, last_name = %s, birthday = %s, phone = %s, email = %s
    WHERE customer_id = %s"""
    
    cursor.execute(update_query, (new_first_name, new_last_name, new_birthday, new_phone, new_email, post_id))
    conn.commit()  
    
    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.index'))


@update_bp.route('/update_pet/<int:post_id>', methods=['POST'])
def update_pet(post_id):

    new_pet_name = request.form.get(f'pet_name_{post_id}')
    new_sex = request.form.get(f'sex_{post_id}')
    new_species = request.form.get(f'species_{post_id}')
    new_birth_year = request.form.get(f'birth_year_{post_id}')
    new_height = request.form.get(f'height_{post_id}')
    new_weight = request.form.get(f'weight_{post_id}')

    # if not new_pet_name and not new_sex and not new_species and not new_birth_year and not new_height and not new_weight:
    #     return "No content to update", 400  
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    update_query = """
    UPDATE pet SET pet_name = %s, sex = %s, species = %s, birth_year = %s, height = %s, weight = %s
    WHERE pet_id = %s"""
    
    cursor.execute(update_query, (new_pet_name, new_sex, new_species, new_birth_year, new_height, new_weight, post_id))
    conn.commit()  
    
    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.index'))


@update_bp.route('/update_appointment/<int:post_id>', methods=['POST'])
def update_appointment(post_id):

    new_appointment_date = request.form.get(f'appointment_date_{post_id}')
    new_appointment_time = request.form.get(f'appointment_time_{post_id}')
    new_purpose = request.form.get(f'purpose_{post_id}')

    # if not new_pet_name and not new_sex and not new_species and not new_birth_year and not new_height and not new_weight:
    #     return "No content to update", 400  
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    update_query = """
    UPDATE appointment SET appointment_date = %s, appointment_time = %s, purpose = %s
    WHERE appointment_id = %s"""
    
    cursor.execute(update_query, (new_appointment_date, new_appointment_time, new_purpose, post_id))
    conn.commit()  
    
    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.index'))


@update_bp.route('/update_service/<int:post_id>', methods=['POST'])
def update_service(post_id):

    new_service_name = request.form.get(f'service_name_{post_id}')
    new_service_type = request.form.get(f'service_type_{post_id}')
    new_description = request.form.get(f'description_{post_id}')
    new_price = request.form.get(f'price_{post_id}')
    new_duration_minutes = request.form.get(f'duration_minutes_{post_id}')

    # if not new_pet_name and not new_sex and not new_species and not new_birth_year and not new_height and not new_weight:
    #     return "No content to update", 400  
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    update_query = """
    UPDATE service SET service_name = %s, service_type = %s, description = %s, price = %s, duration_minutes = %s
    WHERE service_id = %s"""
    
    cursor.execute(update_query, (new_service_name, new_service_type, new_description, new_price, new_duration_minutes, post_id))
    conn.commit()  
    
    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.index'))