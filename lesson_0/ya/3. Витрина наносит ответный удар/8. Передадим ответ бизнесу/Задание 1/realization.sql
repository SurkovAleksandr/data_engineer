-- этот файл не сдаётся, но вы можете использовать его для своего кода

drop materialized view user_activity_payment_datamart;
create materialized view user_activity_payment_datamart as
WITH ual AS (SELECT user_activity_log.client_id,
                    date(min(
                            CASE
                                WHEN user_activity_log.action::text = 'visit'::text THEN user_activity_log.hitdatetime
                                ELSE NULL::timestamp without time zone
                                END)) AS fst_visit_dt,
                    date(min(
                            CASE
                                WHEN user_activity_log.action::text = 'registration'::text
                                    THEN user_activity_log.hitdatetime
                                ELSE NULL::timestamp without time zone
                                END)) AS registration_dt,
                    max(
                            CASE
                                WHEN user_activity_log.action::text = 'registration'::text THEN 1
                                ELSE 0
                                END)  AS is_registration
             FROM user_activity_log
             GROUP BY user_activity_log.client_id),
     upl AS (SELECT user_payment_log.client_id,
                    sum(user_payment_log.payment_amount) AS total_payment_amount
             FROM user_payment_log
             GROUP BY user_payment_log.client_id)
SELECT ua.client_id,
       ua.utm_campaign,
       cl.age,
       ual.fst_visit_dt,
       ual.registration_dt,
       ual.is_registration,
       upl.total_payment_amount
FROM "user_attributes" ua
    left join "002_DM_clients" cl on ua.client_id = cl.client_id
         LEFT JOIN ual ON ua.client_id = ual.client_id
         LEFT JOIN upl ON ua.client_id = upl.client_id;