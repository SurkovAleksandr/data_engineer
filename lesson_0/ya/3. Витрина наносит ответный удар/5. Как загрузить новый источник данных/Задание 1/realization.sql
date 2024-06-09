-- пишите код тут
drop table source_systems;
create table source_systems (
    id int primary key,
    code char(3),
    name varchar(100),
    "desc" varchar(255)
);

insert into source_systems values
    (1,'001','Moscow CRM' ,'Система по работе с клиентами в офисе в Москве'),
    (2,'002','SPB CRM' ,'Система по работе с клиентами в офисе в Санкт-Петербурге'),
    (3,'003','Online shop' ,'Онлайн-магазин компании' );