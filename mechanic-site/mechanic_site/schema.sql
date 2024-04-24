-- Drop existing tables if they exist
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS cars;
DROP TABLE IF EXISTS mechanics;
DROP TABLE IF EXISTS customers;

-- Create customers table
CREATE TABLE customers (
  email VARCHAR(320) PRIMARY KEY,
  name VARCHAR(320) NOT NULL,
  hash TEXT NOT NULL
);

-- Create mechanics table
CREATE TABLE mechanics (
  mechanic_id INTEGER PRIMARY KEY,
  email VARCHAR(320) UNIQUE NOT NULL,
  name VARCHAR(320) NOT NULL,
  zipcode CHAR(10) NOT NULL,
  ein CHAR(10) NOT NULL,
  hash TEXT NOT NULL
);

-- Create cars table
CREATE TABLE cars (
  car_id INTEGER PRIMARY KEY,
  registration VARCHAR(20) UNIQUE NOT NULL,
  owner_email VARCHAR(320) NOT NULL,
  make VARCHAR(100) NOT NULL,
  model_number VARCHAR(100) NOT NULL,
  image_url TEXT,
  FOREIGN KEY (owner_email) REFERENCES customers(email)
);

-- Create appointments table
CREATE TABLE appointments (
  appointment_id INTEGER PRIMARY KEY,
  customer_email VARCHAR(320) NOT NULL,
  mechanic_id INTEGER NOT NULL,
  car_id INTEGER NOT NULL,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL,
  appointment_description TEXT,
  appointment_status INT NOT NULL,
  review_score INT,
  review_text TEXT,
  FOREIGN KEY (customer_email) REFERENCES customers(email),
  FOREIGN KEY (mechanic_id) REFERENCES mechanics(mechanic_id),
  FOREIGN KEY (car_id) REFERENCES cars(car_id)
);