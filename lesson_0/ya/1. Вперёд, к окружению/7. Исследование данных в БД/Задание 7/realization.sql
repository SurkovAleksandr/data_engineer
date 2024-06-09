-- добавьте код сюда
select ua.id, ua.client_id, ua.utm_campaign,
       upl.id, hitdatetime, action, payment_amount
from user_attributes ua
inner join user_payment_log upl using (client_id)
limit 100;