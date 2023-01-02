-- Create database and tables

CREATE DATABASE plant_store;
USE plant_store;

DROP TABLE IF EXISTS catalog, employees_sets_employees, features_sets_features, suppliers_sets_suppliers, plants, warehouses, suppliers, suppliers_sets, features, features_sets, employees, employees_sets;

CREATE TABLE plants (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE warehouses (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE suppliers (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE suppliers_sets (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NULL UNIQUE
);

CREATE TABLE suppliers_sets_suppliers (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    suppliers_set_id INT UNSIGNED NOT NULL,
    supplier_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (suppliers_set_id) REFERENCES suppliers_sets(id) ON UPDATE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON UPDATE CASCADE
);

CREATE TABLE features (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE features_sets (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NULL UNIQUE
);

CREATE TABLE features_sets_features (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    features_set_id INT UNSIGNED NOT NULL,
    feature_id INT UNSIGNED NOT NULL,
    value DOUBLE NULL,
    FOREIGN KEY (features_set_id) REFERENCES features_sets(id) ON UPDATE CASCADE,
    FOREIGN KEY (feature_id) REFERENCES features(id) ON UPDATE CASCADE
);

CREATE TABLE employees (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255) NULL
);

CREATE TABLE employees_sets (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NULL UNIQUE
);

CREATE TABLE employees_sets_employees (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    employees_set_id INT UNSIGNED NOT NULL,
    employee_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (employees_set_id) REFERENCES employees_sets(id) ON UPDATE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON UPDATE CASCADE
);

CREATE TABLE catalog (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    plant_id INT UNSIGNED NOT NULL,
    warehouse_id INT UNSIGNED NOT NULL,
    suppliers_set_id INT UNSIGNED NOT NULL,
    features_set_id INT UNSIGNED NOT NULL,
    employees_set_id INT UNSIGNED NULL,
    FOREIGN KEY (plant_id) REFERENCES plants(id) ON UPDATE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON UPDATE CASCADE,
    FOREIGN KEY (suppliers_set_id) REFERENCES suppliers_sets(id) ON UPDATE CASCADE,
    FOREIGN KEY (features_set_id) REFERENCES features_sets(id) ON UPDATE CASCADE,
    FOREIGN KEY (employees_set_id) REFERENCES employees_sets(id) ON UPDATE CASCADE
);

-- Insert data into them

START TRANSACTION;

INSERT INTO plants (name) VALUES 
    ('Ficus Carica'),
    ('Adenium fat'),
    ('Aglaonema'),
    ('Azalea');
INSERT INTO warehouses (name) VALUES ('No1'), ('No2'), ('No3');
INSERT INTO suppliers (name) VALUES ('UGT'), ('AVDtrade'), ('Flowers of Ukraine'), ('Voloshka');
INSERT INTO features (name) VALUES ('Garden'), ('Closed ground'), ('Indoor'), ('Height');
INSERT INTO employees (first_name, last_name, middle_name) VALUES 
    ('M.', 'Lucyk', 'V.'), 
    ('Y.', 'Stupak', 'K.'),
    ('V.', 'Padik', 'O.');

INSERT INTO suppliers_sets (name) VALUES ('UGT+ACDt Group'), ('AVDt'), ('FoU'), ('Vol');
INSERT INTO suppliers_sets_suppliers (suppliers_set_id, supplier_id) VALUES 
    (1, 1), (1, 2),
    (2, 2),
    (3, 3),
    (4, 4);

INSERT INTO features_sets (name) VALUES ('Gard'), ('Gard Closed'), ('Ind');
INSERT INTO features_sets_features (features_set_id, feature_id, value) VALUES 
    (1, 1, NULL),
    (2, 1, NULL), (2, 2, NULL), (2, 4, 100),
    (3, 3, NULL), (3, 4, 80);

INSERT INTO employees_sets (name) VALUES ('Group 1'), ('Group 2');
INSERT INTO employees_sets_employees (employees_set_id, employee_id) VALUES 
    (1, 1), (1, 2),
    (2, 3);

INSERT INTO catalog (plant_id, warehouse_id, suppliers_set_id, features_set_id, employees_set_id) VALUES 
    (1, 1, 1, 2, 1),
    (2, 2, 2, 3, 2),
    (3, 1, 3, 3, NULL),
    (3, 3, 3, 3, NULL),
    (4, 1, 4, 1, 1);

COMMIT;
