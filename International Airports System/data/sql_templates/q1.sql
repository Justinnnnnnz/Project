-- Q1. Airlines

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO air_travel;
DROP TABLE IF EXISTS q1 CASCADE;

CREATE TABLE q1 (
    pass_id INT,
    name VARCHAR(100),
    airlines INT
);

-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS intermediate_step CASCADE;


-- Define views for your intermediate steps here:


-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q1 
(
(select passenger.id as pass_id, 
	firstname || surname as name, 
	count(distinct airline)
from booking join flight on flight.id = booking.flight_id
			join passenger on passenger.id = booking.pass_id
            join departure on departure.flight_id = booking.flight_id
            join arrival on arrival.flight_id = booking.flight_id
group by passenger.id ) union
(
select passenger.id as pass_id, 
firstname || surname as name, 
	0 as airline
from passenger
where id = 
(

(select passenger.id as id
from passenger
)
EXCEPT 

(
select pass_id as id
	
from booking

)

)

))
;









