-- обновите представление и снова запросите данные за май 2021
refresh materialized view client_activity;

select *
from client_activity
where invoice_month between '2021-05-01' and '2021-05-31';