-- добавьте код сюда
select client_id,
       case when action = 'visit' then hitdatetime end as visit_dt,
       case when action = 'registration' then 1 else 0 end as is_registration
from user_activity_log
limit 10;