-- пишите код тут
select *
from client_activity
where invoice_month between '2021-05-01' and '2021-05-31';

INSERT INTO invoice (customer_id, invoice_date, total)
VALUES (9, DATE '2021-05-01', 2);
