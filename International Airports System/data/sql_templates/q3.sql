-- Q3. North and South Connections

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO air_travel;
DROP TABLE IF EXISTS q3 CASCADE;

CREATE TABLE q3 (
    outbound VARCHAR(30),
    inbound VARCHAR(30),
    direct INT,
    one_con INT,
    two_con INT,
    earliest timestamp
);

-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS intermediate_step CASCADE;


-- Define views for your intermediate steps here:

CREATE TABLE direct_t (
    outbound VARCHAR(30),
    inbound VARCHAR(30),
    num INT

);

CREATE TABLE one_t (
    outbound VARCHAR(30),
    inbound VARCHAR(30),
    num INT

);


CREATE TABLE two_t (
    outbound VARCHAR(30),
    inbound VARCHAR(30),
    num INT

);



CREATE VIEW direct_t as 
select a1.city as outbound, a2.city as inbound, count(*) as num, min(flight.s_arv) as earliest
from flight join airport a1 on flight.outbound = a1.code
			join airport a2 on flight.inbound = a2.code
where (
(a1.country = 'Canada' or a2.country = 'USA')
and(a2.country = 'Canada' or a2.country = 'USA') 
and(a1.country <> a2.country)
and(flight.s_dep > '2022-04-30 00:00:00')
and(flight.s_arv < '2022-04-30 23:59:59')
)
group by a1.city, a2.city
;



CREATE VIEW one_t as 
select a1.city as outbound, a2.city as inbound, count(*) as num,min(f2.s_arv) as earliest
from flight f1 join flight f2 on f1.inbound = f2.outbound
				join airport a1 on f1.outbound = a1.code
				join airport a2 on f2.inbound = a2.code
            
where (
(a1.country = 'Canada' or a2.country = 'USA')
and(a2.country = 'Canada' or a2.country = 'USA') 
and(a1.country <> a2.country)
and(f1.s_dep > '2022-04-30 00:00:00')
and(f2.s_arv < '2022-04-30 23:59:59')
)
group by a1.city, a2.city
;

CREATE VIEW two_t as 
select a1.city as outbound, a2.city as inbound, count(*) as num,min(f3.s_arv) as earliest
from flight f1 join flight f2 on f1.inbound = f2.outbound
				join flight f3 on f2.inbound = f3.outbound
				join airport a1 on f1.outbound = a1.code
				join airport a2 on f3.inbound = a2.code
            
where (
(a1.country = 'Canada' or a2.country = 'USA')
and(a2.country = 'Canada' or a2.country = 'USA') 
and(a1.country <> a2.country)
and(f1.s_dep > '2022-04-30 00:00:00')
and(f3.s_arv < '2022-04-30 23:59:59')
)
group by a1.city, a2.city
;

-- pair city 

CREATE VIEW pairs as
(
select outbound, inbound
from
(select distinct city as outbound from airport where country = 'Canada') as aa,
 (select distinct city as inbound from airport where country = 'USA') as bb)
 union
 (
 select outbound, inbound
from
 (select distinct city as outbound from airport where country = 'USA') as cc,
 (select distinct city as inbound from airport where country = 'Canada') as dd
);



-- Your query that answers the question goes below the "insert into" line: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
-- INSERT INTO q3

select  outbound, inbound, sum(direct), sum(one_con), sum(two_con), min(earliest)
from (
(select  pairs.outbound as outbound, pairs.inbound as inbound, 0 as direct, 0 as one_con, 0 as two_con, null as earliest
from pairs
where  ( (pairs.outbound not in ( select outbound from direct_t))
and (pairs.inbound not in ( select inbound from direct_t))    )
and 
( (pairs.outbound not in ( select outbound from one_t))
and (pairs.inbound not in ( select inbound from one_t))    )
and 
( (pairs.outbound not in ( select outbound from two_t))
and (pairs.inbound not in ( select inbound from two_t))    )
)
union

(select outbound, inbound, num as direct, 0 as one_con, 0 as two_con, earliest
from  direct_t
)

union 

(
select outbound, inbound, 0 as direct, num as one_con, 0 as two_con, earliest
from  one_t
)

union

(select outbound, inbound, 0 as direct, 0 as one_con, num as two_con, earliest
from  two_t
)
) as temp

group by outbound, inbound

;

