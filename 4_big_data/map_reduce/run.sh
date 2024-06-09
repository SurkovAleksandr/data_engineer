export MR_OUTPUT=/home/ubuntu/output-data

hadoop fs -rm -r $MR_OUTPUT


hadoop jar "$HADOOP_MAPRED_HOME"/hadoop-streaming.jar \
-Dmapred.job.name='Simple streaming job reduce' \
-Dmapred.reduce.tasks=1 \
-Dmapreduce.input.lineinputformat.linespermap=1000 \
-inputformat org.apache.hadoop.mapred.lib.NLineInputFormat \
-file /home/ubuntu/map_reduce/mapper.py -mapper /home/ubuntu/map_reduce/mapper.py \
-file /home/ubuntu/map_reduce/reducer.py -reducer /home/ubuntu/map_reduce/reducer.py \
-input /user/ubuntu/input-data -output $MR_OUTPUT

# Вопросы
- место определения переменной -Dmapred.reduce.tasks=1 влияет на выполнение команты
- что приходит в reduce метод
- куда указывают параметры -file и -mapper(-reducer)
- minRecWrittenToEnableSkip_=9223372036854775807 HOST=null
  USER=ubuntu
  HADOOP_USER=null
  last tool output: |['li', 'n\te']|
  Stream closed



# Опции(похоже порядок важен - команда иначе не запускается):
# -file - перечисленные через запятую файлы(или помечать каждый файл этой опцией), которые надо скопировать на map-reduce кластер
# -Dmapred.reduce.tasks=1 - количество редьюсеров

# -Dmapred.reduce.tasks=1 \
#-Dmapreduce.input.lineinputformat.linespermap=1000 \
#-inputformat org.apache.hadoop.mapred.lib.NLineInputFormat \


#-Dmapred.job.name='Simple streaming job' \
#-Dmapred.reduce.tasks=1 -Dmapreduce.input.lineinputformat.linespermap=1000 \
#-inputformat org.apache.hadoop.mapred.lib.NLineInputFormat \


# -inputformat org.apache.hadoop.mapred.lib.NLineInputFormat -Dmapreduce.input.lineinputformat.linespermap=1000 \

## s3
# -Dfs.s3a.endpoint=s3.amazonaws.com -Dfs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider


#hadoop fs -rm -r taxi-output
#
#hadoop jar "$HADOOP_MAPRED_HOME"/hadoop-streaming.jar \
#-Dmapred.job.name='Taxi streaming job' \
#-Dmapred.reduce.tasks=10 \
#-Dmapreduce.map.memory.mb=1024 \
#-file /tmp/mapreduce/mapper.py -mapper /tmp/mapreduce/mapper.py \
#-file /tmp/mapreduce/reducer.py -reducer /tmp/mapreduce/reducer.py \
#-input /user/root/2019  -output taxi-output


hadoop jar "$HADOOP_MAPRED_HOME"/hadoop-streaming.jar \
-Dmapred.job.name='Simple streaming job reduce' \
-Dmapred.reduce.tasks=1 \
-Dmapreduce.input.lineinputformat.linespermap=10000 \
-inputformat org.apache.hadoop.mapred.lib.NLineInputFormat \
-file /home/ubuntu/map_reduce/mapper.py -mapper /home/ubuntu/map_reduce/mapper.py \
-file /home/ubuntu/map_reduce/reducer.py -reducer /home/ubuntu/map_reduce/reducer.py \
-input /user/ubuntu/input-data -output $MR_OUTPUT


hadoop jar "$HADOOP_MAPRED_HOME"/hadoop-streaming.jar \
-Dmapred.job.name='Taxi job reduce' \
-Dmapred.reduce.tasks=1 \
-Dmapreduce.input.lineinputformat.linespermap=10000 \
-inputformat org.apache.hadoop.mapred.lib.NLineInputFormat \
-file /home/ubuntu/taxi/map_taxi.py -mapper /user/ubuntu/taxi_map_reduce/map_taxi.py \
-file /home/ubuntu/taxi/reducer_taxi.py -reducer /user/ubuntu/taxi_map_reduce/reducer_taxi.py \
-input /user/ubuntu/taxi -output $MR_OUTPUT

hadoop jar "$HADOOP_MAPRED_HOME"/hadoop-streaming.jar \
-Dmapred.job.name='Taxi job reduce' \
-Dmapred.reduce.tasks=1 \
-Dmapreduce.input.lineinputformat.linespermap=100000 \
-inputformat org.apache.hadoop.mapred.lib.NLineInputFormat \
-file /home/ubuntu/taxi/map_taxi.py -mapper /home/ubuntu/taxi/map_taxi.py \
-file /home/ubuntu/taxi/reducer_taxi.py -reducer /home/ubuntu/taxi/reducer_taxi.py \
-input /user/ubuntu/taxi -output $MR_OUTPUT

hadoop jar "$HADOOP_MAPRED_HOME"/hadoop-streaming.jar \
-Dmapred.job.name='Taxi job reduce' \
-Dmapred.reduce.tasks=1 \
-Dmapreduce.input.lineinputformat.linespermap=3000000 \
-inputformat org.apache.hadoop.mapred.lib.NLineInputFormat \
-file /home/ubuntu/taxi_map_reduce/map_taxi.py -mapper /home/ubuntu/taxi_map_reduce/map_taxi.py \
-file /home/ubuntu/taxi_map_reduce/reduce_taxi.py -reducer /home/ubuntu/taxi_map_reduce/reduce_taxi.py \
-input /user/ubuntu/taxi -output $MR_OUTPUT