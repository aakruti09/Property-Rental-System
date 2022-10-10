-- Case 1 : 
-- To clean the host_listings_count attribute of Host
UPDATE Host SET host_listings_count=0 WHERE host_id NOT IN (SELECT DISTINCT host_id FROM Property);

WITH T1 AS (SELECT host_id,count(host_id) AS cnt,host_listings_count FROM Property INNER JOIN Host USING (host_id) GROUP BY host_id HAVING cnt <> host_listings_count)
UPDATE T1 INNER JOIN Host USING(host_id) SET Host.host_listings_count=T1.cnt;

-- Test should return Empty set
SELECT host_id,count(host_id) AS cnt,host_listings_count FROM Property INNER JOIN Host USING (host_id) GROUP BY host_id HAVING cnt <> host_listings_count;


-- Case 2 : 
-- Count of distinct number of host from Property should be greater than or equal to row count in host. As if there is property, then there should be compulsory host. Its possible that host does not have any property yet. 

WITH T1 AS (SELECT count(distinct host_id) AS cnt_host_from_property FROM Property),
T2 AS (SELECT count(host_id) AS cnt_hostid_from_host FROM Host) 
SELECT * from T1,T2;

-- Case 3 :
-- User can only provide review on properties that they have booked and checked out and once per booking
-- Executing this query should give an Error "ERROR: Cannot add or update a child row: a foreign key constraint fails"
insert into Review (booking_id, date_of_review, comments) values ((select max(booking_id)+1 from Booking), "2021-12-23", "Testing review.");

