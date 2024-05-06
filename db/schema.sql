CREATE DATABASE IF NOT EXISTS metrics_db;

USE metrics_db;

CREATE TABLE IF NOT EXISTS metrics (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  name TEXT NOT NULL,
  value REAL NOT NULL,
  timestamp TIMESTAMP NOT NULL
);

CREATE USER 'user'@'%' IDENTIFIED BY 'pwd';
GRANT SELECT,INSERT ON metrics_db.metrics TO 'user'@'%';
GRANT PROCESS ON *.* TO 'user'@'%';
