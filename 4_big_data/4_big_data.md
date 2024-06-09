[Материал по практикам на GitLab](https://git.lab.karpov.courses/de/spark)

### Основные команды

Команда         Пример
- appendToFile  hdfs dfs -appendToFile localfile /user/hadoop/hadoopfile
- cat         	hdfs dfs -cat hdfs://nn1.example.com/file1
- copyFromLocal hdfs dfs -copyFromLocal localfile /user/hadoop/data/
- copyToLocal   hdfs dfs -copyToLocal localfile /tmp/data/ localfile
- cp          	hdfs dfs -cp [-f] [-p | -p[topax]] URI [URI ...] <dest>
- du          	hdfs dfs -du -s /tmp/test.data
- expunge       hdfs dfs -expunge
- get         	hdfs dfs -get /user/hadoop/file localfile
- getmerge      hdfs dfs -getmerge <src> <localdst> [addnl]
- ls          	hdfs dfs -ls /user/hadoop/file1
- mkdir         hdfs dfs -mkdir /user/hadoop/dir1 /user/hadoop/dir2
- mv          	hdfs dfs -mv /user/hadoop/file1 /user/hadoop/file2
- put         	hdfs dfs -put localfile /user/hadoop/hadoopfile
- rm          	hdfs dfs -rm [-f] [-r|-R] [-skipTrash] URI [URI ...]
- tail          hdfs dfs -tail pathname
- setrep        hdfs dfs -setrep [-R] [-w] <numReplicas> <path>


### Урок 2 - Создание кластера
`ssh ubuntu@<скопированный адрес>`
`ssh -i /path/to/ssh_key ubuntu@<скопированный адрес>`

-- после входа на мастер ноду надо создать папку. 
Если нет прав: mkdir: Cannot create directory /user/ubuntu. Name node is in safe mode.
то добавить права на кореть /

`sudo -u hdfs hadoop fs -chmod 777 /
sudo -u ubuntu hdfs dfs -mkdir /user
sudo -u ubuntu hdfs dfs -mkdir /user/ubuntu`

`hadoop fs -mkdir /user/ubuntu`
`hdfs dfsadmin -safemode get`
`hadoop fs -ls /`

- Пример вывода, когда количество репликаций больше чем датанод
```shell
ubuntu@rc1a-dataproc-m-6s631ayckob7llwe:~$ hdfs fsck hello.txt -files -blocks -locations
Connecting to namenode via http://rc1a-dataproc-m-6s631ayckob7llwe.mdb.yandexcloud.net:9870/fsck?ugi=ubuntu&files=1&blocks=1&locations=1&path=%2Fuser%2Fubuntu%2Fhello.txt
FSCK started by ubuntu (auth:SIMPLE) from /10.128.0.30 for path /user/ubuntu/hello.txt at Thu Mar 21 19:56:51 UTC 2024

/user/ubuntu/hello.txt 12 bytes, replicated: replication=2, 1 block(s):  Under replicated BP-939974075-10.128.0.30-1710958132838:blk_1073741843_1019. 
Target Replicas is 2 but found 1 live replica(s), 0 decommissioned replica(s), 0 decommissioning replica(s).
0. BP-939974075-10.128.0.30-1710958132838:blk_1073741843_1019 len=12 Live_repl=1  [DatanodeInfoWithStorage[10.128.0.14:9866,DS-0e40f2c4-75f5-47b8-9bc7-cd672e5122d7,DISK]]
```

- Пример вывода, когда количество репликаций **не** больше чем датанод
```shell
ubuntu@rc1a-dataproc-m-6s631ayckob7llwe:~$ hdfs fsck hello.txt -files -blocks -locations
Connecting to namenode via http://rc1a-dataproc-m-6s631ayckob7llwe.mdb.yandexcloud.net:9870/fsck?ugi=ubuntu&files=1&blocks=1&locations=1&path=%2Fuser%2Fubuntu%2Fhello.txt
FSCK started by ubuntu (auth:SIMPLE) from /10.128.0.30 for path /user/ubuntu/hello.txt at Sat Mar 23 12:29:23 UTC 2024

/user/ubuntu/hello.txt 12 bytes, replicated: replication=2, 1 block(s):  OK
0. BP-939974075-10.128.0.30-1710958132838:blk_1073741843_1019 len=12 Live_repl=2  [DatanodeInfoWithStorage[10.128.0.14:9866,DS-0e40f2c4-75f5-47b8-9bc7-cd672e5122d7,DISK], DatanodeInfoWithStorage[10.128.0.12:9866,DS-f284a75c-0353-4df6-8490-5ffe27de7f18,DISK]]

```

### [AWS](https://lab.karpov.courses/learning/355/module/3433/lesson/30413/85497/400871/)
Конфигурация для AWS - `aws configure`
```text
- AWS_ACCESS_KEY -- YCAJE4TCZS0bvp70fMrGGG-Lh
- AWS_SECRET_KEY -- YCNHXtzvdyecxcaZfsT3THwFLQlhbLcUmk-MZ6kd
- REGION -- ru-central1
- OUTPUT_FORMAT -- json
```

```shell
aws --endpoint-url=https://storage.yandexcloud.net s3 ls s3://ny-taxi-data/ny-taxi/
или с профилем
aws --profile=karpov-user --endpoint-url=https://storage.yandexcloud.net s3 ls s3://ny-taxi-data/ny-taxi/
```
Дарлее --profile=karpov-user убран, т.к. настраивал профиль по умолчанию
```shell
aws --endpoint-url=https://storage.yandexcloud.net s3 cp s3://ny-taxi-data/ny-taxi/yellow_tripdata_2020-12.csv ./
```
Загрузим скачанный файл на HDFS с размером блока 64Мб и двойной репликацией:
```shell
hadoop fs -Ddfs.blocksize=67108864 -Ddfs.replication=2 -put yellow_tripdata_2020-12.csv
или
hdfs dfs -Ddfs.blocksize=67108864 -Ddfs.replication=2 -put yellow_tripdata_2020-12.csv
```

Копирование всех файлов к себе локально
```shell
aws --endpoint-url=https://storage.yandexcloud.net s3 cp --recursive s3://ny-taxi-data/ny-taxi/ ./2020
```

И следующим шагом переложим их на HDFS тоже в директорию 2020:

```shell
hadoop fs -put /ubuntu/2020 2020
```

Так, чтобы вывести первые 10 строчек выполним:
```shell
hadoop fs -text 2020/yellow_tripdata_2020-10.csv | head -n 10
```

Чтобы посмотреть данные в конце файла воспользуемся tail:
```shell
hadoop fs -tail 2020/yellow_tripdata_2020-10.csv
```


### Задание 
 - [Задание](https://lab.karpov.courses/learning/355/module/3433/lesson/30415/85505/400913/)
 - [загрузка данных через S3](https://lab.karpov.courses/learning/355/module/3433/lesson/30413/85497/400871/)