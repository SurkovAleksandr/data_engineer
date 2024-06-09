-- пишите код тут
drop table "002_DM_clients";
create table "002_DM_clients" (
     client_id int primary key ,
     client_firstname varchar(200),
     client_lastname varchar(200),
     client_email varchar(200),
     client_phone varchar(200),
     client_city varchar(200)
);