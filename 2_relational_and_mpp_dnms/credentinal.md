1. БД
   1. Имя базы данных для создания: training_pg
   2. Имя пользователя/Пароль пользователя: user/2eWFY5,e0J1452K4E

```shell
cat /home/gpadmin/supplier.txt | psql "host=<IP-ADDRESS> port=<PORT> sslmode=verify-full dbname=db1 user=user1 target_session_attrs=read-write" -c "copy supplier from stdin with (DELIMITER '|');"

# Пример
de_2=# \copy customer from './2_relational_and_mpp_dnms/3 Урок 4 Задание HomeWork_Files/customer.json' with (delimiter '|');
```

```sql
-- Определение распределение данных по кластеру Greenplum
select gp_segment_id, count(*) from gp_dist_random('tpch1.customer') group by 1;

-- От распределения зависит скорость выполнения запросов(пример - https://lab.karpov.courses/learning/355/module/3431/lesson/30397/85443/400696/)
-- Помимо распределения записей по сегментам необходимо учитывать каким образом происходит распределение.
-- Может происходить рандомно - distributed randomly;
-- а может происходить по ключу - distributed by (c_custkey);
-- Если по этому ключу происходит распределение и в другой таблице, то join этих таблиц 
-- по этому ключу будет происходить быстрее.
```

### [Оконные функции](https://lab.karpov.courses/learning/355/module/3431/lesson/30398/85446/400702/)
#### Агрегатные функции
Позволяют за одно чтение данных с диска произвести всевозможные вычисления и выдать нужный результат, что сильно ускоряет время действия запроса.

- COUNT - подсчитывает количество входных строк
- SUM - сумма всех непустых входных значений
- MIN/MAX -  минимум/максимум среди всех непустых входных значений
- AVG - арифметическое среднее всех непустых входных значений

Расширенный набор агрегатных функций:
- MEDIAN - вычисляет медиану среди всех непустых входных значений
- PERCENTILE_COUNT/PERCENTILE_DISC - вычисляет процентиль для непрерывного/дискретного распределения
- SUM(array[]) - позволяет производить суммирование списков (суммирование ведется со соответсвующим индексам)


####
- FIRST_VALUE/LAST_VALUE - позволяют в рамках окна найти соответственно первое и последнее значение
- LAG/LEAD - позволяют работать со строками, которые находятся на некотором расстоянии от текущей позиции в рассматриваемом окне
- CUME_DIST - позволяет создать функцию распределения
- RANK/DENSE_RANK - ранг текущей строки с пропусками / без пропусков
- ROW_NUMBER - номер текущей строки в её разделе
- PERCENT_RANK - относительный ранг текущей строки

### JSON

| Operator | Type   | Description                                     | Example                                         | Result       |
|----------|--------|-------------------------------------------------|-------------------------------------------------|--------------|
| ->	     | int    | Get the JSON array element (indexed from zero).| '[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json->2| {"c":"baz"}  |
| ->	     | text   | Get the JSON object field by key.	           | '{"a": {"b":"foo"}}'::json->'a'	             | {"b":"foo"}  |
| ->>      | int    | Get the JSON array element as text.	           | '[1,2,3]'::json->>2	                         | 3            |
| ->>      | text   | Get the JSON object field as text.	           | '{"a":1,"b":2}'::json->>'b'	                 | 2            |
| #>	    | text[] | Get the JSON object at specified path.	       | '{"a": {"b":{"c": "foo"}}}'::json#>'{a,b}'	     | {"c": "foo"} |
| #>>      | text[] | Get the JSON object at specified path as text.  | '{"a":[1,2,3],"b":[4,5,6]}'::json#>>'{a,2}'	 | 3            |


#### Ссылки на документации:
<ul>
<li><a href="https://www.postgresql.org/docs/9.4/functions-aggregate.html">аналитические функции</a></li>
<li><a href="https://docs.vmware.com/en/VMware-Greenplum/6/greenplum-database/ref_guide-function-summary.html?hWord=N4IghgNiBc4HaQJ4BcCWBjSACAZgVznTQHs4BnEAXyA#topic31">расширенные функции агрегирования</a></li>
<li><a href="https://docs.vmware.com/en/VMware-Greenplum/6/greenplum-database/analytics-pl_container.html">про PL/Container</a></li>
<li><a href="https://docs.vmware.com/en/VMware-Greenplum/6/greenplum-database/admin_guide-query-topics-json-data.html">преобразование json</a></li>
<li><a href="https://docs.vmware.com/en/VMware-Greenplum/6/greenplum-database/admin_guide-query-topics-xml-data.html">преобразование xml</a></li>
<li><a href="https://docs.vmware.com/en/VMware-Greenplum/6/greenplum-database/analytics-madlib.html">MADlib</a></li>
<li><a href="https://postgis.net/docs/">PostGIS</a></li>
<li><a href="https://docs.vmware.com/en/VMware-Greenplum/6/greenplum-database/admin_guide-textsearch-intro.html">GreenPlum Database Full Text Search</a></li>
</ul>
