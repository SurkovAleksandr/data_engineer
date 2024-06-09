select case
           when cl.age >= 18 and cl.age <= 25 then '18-25'
           when cl.age >= 26 and cl.age <= 30 then '26-30'
           when cl.age >= 31 and cl.age <= 40 then '31-40'
           when cl.age >= 41 and cl.age <= 55 then '41-55'
           when cl.age > 55 then '55+'
           end as age_name,
       sum(payment_amount) amount
from "002_DM_clients" cl
         left join user_payment_log upl on cl.client_id = upl.client_id
where cl.age is not null
and upl.action in (
        'accept-method',
        'make-payment',
        'open-paystation',
        'choose-method'
    )
group by age_name
order by amount desc
;