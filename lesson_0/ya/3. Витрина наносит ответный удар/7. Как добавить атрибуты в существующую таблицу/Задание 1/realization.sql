-- напишите тут запрос
alter table "002_DM_clients" add column age int ;

update "002_DM_clients" as t 
set age = s.age
from "002_BUFF_clients" as s
where t.client_id = s.client_id;