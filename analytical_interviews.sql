DROP TABLE analytic_first_interview;

-- create new analytical table
CREATE TABLE analytic_first_interview(
	appointment_id int PRIMARY KEY,
	candidate_reference_id int,
	candidate_name varchar(200),
	email varchar(200),
	category_name varchar(200),
	desired_locations varchar(200),
	type varchar(200),
	owner_id int,
	date_begin DATETIME,
	date_begin_key int,
	job_submission_id int,
	job_order_id int,
	title varchar(200),
	status varchar(200)
);

--insert data into above table
INSERT INTO analytic_first_interview (appointment_id, candidate_reference_id,
candidate_name, email, category_name, desired_locations, type,  owner_id, date_begin, date_begin_key, job_submission_id, job_order_id, title, status)
-- select fields for table
SELECT
a.appointment_id,
a.candidate_reference_id,
dbo.InitCap(CONCAT(c.first_name,' ', c.last_name)) AS candidate_name, --combine into one name column
c.email,
c.category_name,
c.desired_locations,
a.type,
a.owner_id,
date_begin,
FORMAT(a.date_begin,'yyyyMMdd') as date_begin_key, --create date key to join date dimension table
a.job_submission_id,
a.job_order_id,
v.title,
CASE
	WHEN UPPER(type) = 'FINAL INTERVIEW' THEN 'Final Interview'
	WHEN UPPER(type) = 'TRIAL DAY' THEN 'Final Interview'
	WHEN UPPER(type) = 'INTERVIEW' THEN 'First Interview'
END status
from test_appointment a
left join recruiters_dim o on o.owner_id = a.owner_id
left join test_vacancy v on a.job_order_id = v.vacancy_id
left join test_candidates c on c.candidate_id = a.candidate_reference_id
WHERE (UPPER(type) LIKE '%INTERVIEW%' OR UPPER(type) LIKE 'TRIAL%') AND --look at interviews and trial days
candidate_reference_id IS NOT NULL;