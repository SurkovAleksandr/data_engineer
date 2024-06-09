-- пишите код тут

select *
from client_activity
where invoice_month between '2021-06-01' and '2021-06-30';

INSERT INTO invoice (customer_id, invoice_date, total)
VALUES (9, DATE '2021-06-01', 2);

select *
from client_activity
where invoice_month between '2021-06-01' and '2021-06-30';