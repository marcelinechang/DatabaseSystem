USE `test_db`;

DROP TABLE IF EXISTS `pet`;
CREATE TABLE `pet` (
  `pet_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `pet_name` varchar(100) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `species` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_updated_at` timestamp ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `customer_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `birthday` DATE,
  `phone` varchar(10) NOT NULL,
  `email` varchar(100),
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_updated_at` timestamp ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `appointment`;
CREATE TABLE `appointment` (
    appointment_id VARCHAR(20) PRIMARY KEY,
    pet_id int NOT NULL,
    owner_id varchar(100) NOT NULL,
    appointment_date DATE,
    appointment_time TIME,
    purpose int,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `order_counter`;
CREATE TABLE `order_counter` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    counter INT NOT NULL
);



DELIMITER //

CREATE TRIGGER before_insert_orders
BEFORE INSERT ON appointment
FOR EACH ROW
BEGIN
    DECLARE new_counter INT;
    
    -- 自增計數器
    INSERT INTO order_counter (counter) VALUES (0);
    SET new_counter = LAST_INSERT_ID();

    -- 生成訂單編號：時間戳 + 自增編號
    SET NEW.appointment_id = CONCAT(DATE_FORMAT(NEW.created_at, '%Y%m%d%H%i%s'), LPAD(new_counter, 6, '0'));
END //

DELIMITER ;


DROP TABLE IF EXISTS `service`;
CREATE TABLE `service` (
    service_id INT AUTO_INCREMENT PRIMARY KEY, 
    service_name VARCHAR(255) NOT NULL,
    service_type VARCHAR(20) NOT NULL,
    `description` TEXT,
    price INT NOT NULL, 
    duration_minutes INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB AUTO_INCREMENT= 11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;






