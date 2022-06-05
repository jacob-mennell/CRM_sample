--define view
CREATE VIEW dbo.analytical_interviews_VIEW AS

--select statement
a.appointment_id,
a.candidate_reference_id,
dbo.InitCap(CONCAT(c.first_name,' ', c.last_name)) AS candidate_name, --single name field
c.email,
c.category_name,
c.desired_locations,
a.type,
a.owner_id,
date_begin,
FORMAT(a.date_begin,'yyyyMMdd') as date_begin_key, --join to date dim table
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
WHERE (UPPER(type) LIKE '%INTERVIEW%' OR UPPER(type) LIKE 'TRIAL%') AND
candidate_reference_id IS NOT NULL;