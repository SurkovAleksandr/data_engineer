-- Поменяйте этот код
select client_id,
       min(case when action = 'visit' then hitdatetime end) as fst_visit_dt,
       min(case when action = 'registration' then hitdatetime end) as registration_dt,
       max(case when action = 'registration' then 1 else 0 end) as is_registration
from user_activity_log
group by client_id
limit 10;;