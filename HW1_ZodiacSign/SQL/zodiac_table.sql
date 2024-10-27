-- CREATE DATABASE IF NOT EXISTS `test_db`;

USE test_db;
DROP TABLE IF EXISTS `zodiac`;
CREATE TABLE `zodiac` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nickname` varchar(100) NOT NULL,
  `zodiac_sign` varchar(15) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Add Column [last_updated_at]
ALTER TABLE test_db.zodiac ADD COLUMN last_updated_at datetime;

-- Alter Column [last_updated_at] and Check Result
ALTER TABLE test_db.zodiac
MODIFY last_updated_at timestamp ON UPDATE CURRENT_TIMESTAMP;

SELECT * FROM test_db.zodiac