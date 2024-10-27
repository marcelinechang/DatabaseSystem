SELECT appointment_id, pet_name, species,
CONCAT(first_name, " ", last_name) AS owner_name, phone,
appointment_date AS date, appointment_time AS time, service_name AS service
FROM appointment
LEFT JOIN pet ON appointment.pet_id = pet.pet_id
LEFT JOIN customer ON appointment.owner_id = customer.customer_id
LEFT JOIN service ON appointment.purpose = service.service_id
WHERE appointment_date BETWEEN CURDATE() AND CURDATE() + 7
ORDER BY appointment_date, appointment_time