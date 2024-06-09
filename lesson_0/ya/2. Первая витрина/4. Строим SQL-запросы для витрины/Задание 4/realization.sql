-- Поменяйте этот код
with empt as (
      select * from user_attributes ua
)
select client_id,
       utm_campaign,
       min(case when ual.action = 'visit' then ual.hitdatetime end) as fst_visit_dt,
       min(case when ual.action = 'registration' then ual.hitdatetime end) as registration_dt,
       max(case when ual.action = 'registration' then 1 else 0 end) as is_registration,
       sum(upl.payment_amount) as total_payment_amount
from user_attributes ua
left join user_activity_log ual using (client_id)
left join user_payment_log upl using (client_id)
group by client_id, utm_campaign
limit 10;