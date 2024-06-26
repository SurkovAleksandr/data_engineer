-- Этот запрос должен стать представлением
drop view client_activity;
create materialized view client_activity as (
  WITH i AS (
      SELECT customer_id,
             DATE_TRUNC('month', CAST(invoice_date AS timestamp)) AS invoice_month,
             total
      FROM invoice
  )
  SELECT i.customer_id,
         client.company IS NOT NULL AS is_from_company,
         i.invoice_month,
         COUNT(i.total),
         SUM(i.total)
  FROM i
  LEFT JOIN client ON i.customer_id = client.customer_id
  GROUP BY i.customer_id, i.invoice_month, client.company
  having sum(i.total) > 1
  )
;