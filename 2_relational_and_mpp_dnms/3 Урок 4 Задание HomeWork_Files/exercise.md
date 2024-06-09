select count(*), round(avg(c_acctbal),2) from customer
UNION
select count(*), round(avg(n_regionkey),2) from nation
UNION
select count(*), round(avg(p_retailprice),2) from part
UNION
select count(*), round(avg(ps_supplycost),2) from partsupp
UNION
select count(*), round(avg(r_regionkey),2) from region
UNION
select count(*), round(avg(s_acctbal),2) from supplier;

\copy nation from './2_relational_and_mpp_dnms/3 Урок 4 Задание HomeWork_Files/nation.txt' with (delimiter '|');
\copy part from './2_relational_and_mpp_dnms/3 Урок 4 Задание HomeWork_Files/part.txt' with (delimiter '|');
\copy partsupp from './2_relational_and_mpp_dnms/3 Урок 4 Задание HomeWork_Files/partsupp.txt' with (delimiter '|');
\copy partsupp1 from './2_relational_and_mpp_dnms/3 Урок 4 Задание HomeWork_Files/partsupp1.txt' with (delimiter '|');
\copy partsupp2 from './2_relational_and_mpp_dnms/3 Урок 4 Задание HomeWork_Files/partsupp2.txt' with (delimiter '|');
\copy region from './2_relational_and_mpp_dnms/3 Урок 4 Задание HomeWork_Files/region.txt' with (delimiter '|');
\copy supplier from './2_relational_and_mpp_dnms/3 Урок 4 Задание HomeWork_Files/supplier.txt' with (delimiter '|');


