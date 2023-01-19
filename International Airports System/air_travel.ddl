-- Air Travel Schema.

DROP SCHEMA IF EXISTS air_travel CASCADE;
CREATE SCHEMA air_travel;
SET SEARCH_PATH to air_travel;

-- A passenger who flies.
CREATE TABLE Passenger (
  id INT PRIMARY KEY,
  -- The first name of the passenger.
  firstname VARCHAR(50) NOT NULL,
  -- The surname of the passenger.
  surname VARCHAR(50) NOT NULL,
  -- The email of the passenger.
  email varchar(30) NOT NULL
);

CREATE TABLE Airport (
  -- 3-letter airport code.
  code CHAR(3) PRIMARY KEY,
  -- the airport name
  name VARCHAR(100) NOT NULL,
  -- the airport city
  city VARCHAR(30) NOT NULL,
  -- the airport country
  country VARCHAR(30) NOT NULL
);

CREATE TABLE Airline (
  -- two-character airline code
  code CHAR(2) PRIMARY KEY,
  -- name of the airline
  name VARCHAR(50) NOT NULL
);

CREATE TABLE Plane (
  -- the unique identifier of the plane
  tail_number CHAR(5) PRIMARY KEY,
  -- the airline that the plane belongs to
  airline CHAR(2) NOT NULL REFERENCES Airline,
  -- the model of the plane
  model VARCHAR(20) NOT NULL,

  -- passenger capacities for economy, business, and first class
  capacity_economy INT NOT NULL,
  capacity_business INT NOT NULL,
  capacity_first INT NOT NULL
);


CREATE TABLE Flight (
  id INT PRIMARY KEY,
  -- airline that offers the flight
  airline CHAR(2) NOT NULL REFERENCES airline,
  -- the flight number
  flight_num INT NOT NULL,
  plane CHAR(5) NOT NULL REFERENCES Plane,
  -- the outbound airport (departure airport)
  outbound CHAR(3) NOT NULL REFERENCES Airport,
  -- the inbound airport (arrival airport)
  inbound CHAR(3) NOT NULL REFERENCES Airport,
  -- The scheduled departure time of the flight
  s_dep timestamp NOT NULL,
  -- The scheduled arrival time of the flight.
  s_arv timestamp NOT NULL
);

-- The actual recorded flight departure times.
CREATE TABLE Departure (
  flight_id INT PRIMARY KEY REFERENCES Flight,
  datetime timestamp NOT NULL
);

-- The actual recorded flight arrival times.
CREATE TABLE Arrival (
  flight_id INT PRIMARY KEY REFERENCES Departure,
  datetime timestamp NOT NULL
);

-- Passenger flight bookings.
CREATE TYPE seat_class AS ENUM ('economy', 'business', 'first');
CREATE TABLE Booking (
  id INT PRIMARY KEY,
  -- passenger and flight for the booking
  pass_id INT REFERENCES Passenger,
  flight_id INT REFERENCES Flight,
  -- timestamp of when booking was made
  datetime timestamp NOT NULL,
  -- the price at the time of booking (not necessarily the price in the Price table at any given time).
  price DECIMAL NOT NULL,

  -- seat information
  seat_class seat_class NOT NULL,
  row INT,
  letter CHAR(1)
);

-- The current market price for tickets for each seat class.
-- In reality, these prices are updated often.
CREATE TABLE Price (
    flight_id INT PRIMARY KEY REFERENCES Flight,
    -- Prices for economy, business, and first class for a flight
    economy INT,
    business INT,
    first INT
);

-- Parameters for Query 5 (guaranteed only one row in this table).
CREATE TABLE q5_parameters (
  -- the date to start flight hopping
  day timestamp,
  -- the maximum number of flights from YYZ
  n INT
);


-- Data loaded in from CSV files.
\COPY passenger FROM 'passenger.csv' DELIMITER ',' CSV header;
\COPY airport FROM 'airport.csv' DELIMITER ',' CSV header;
\COPY airline FROM 'airline.csv' DELIMITER ',' CSV header;
\COPY plane FROM 'plane.csv' DELIMITER ',' CSV header;
\COPY flight FROM 'flight.csv' DELIMITER ',' CSV header;
\COPY departure FROM 'departure.csv' DELIMITER ',' CSV header;
\COPY arrival FROM 'arrival.csv' DELIMITER ',' CSV header;
\COPY booking FROM 'booking.csv' DELIMITER ',' CSV header;
\COPY price FROM 'price.csv' DELIMITER ',' CSV header;
\COPY q5_parameters FROM 'q5_parameters.csv' DELIMITER ',' CSV header;
