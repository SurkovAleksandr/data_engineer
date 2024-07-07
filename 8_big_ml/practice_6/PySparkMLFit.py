# Практическое задание 6 - https://lab.karpov.courses/learning/355/module/3437/lesson/30466/85654/401562/
# шаблон для процесса обучения вашей модели, задача должна создавать план обучения модели с учетом оптимизации гиперпараметров,
# определять лучшую модель и сохранять ее для дальнейшего использования.
# Параметры запуска задачи:
# data_path - путь к файлу с данными
# model_path - путь куда будет сохранена модель

# Строка запуска:
# python PySparkMLFit.py --data_path=session-stat.parquet --model_path=spark_ml_model
# ИЛИ
#spark-submit PySparkMLFit.py --data_path=session-stat.parquet --model_path=spark_ml_model

# Эталонная реализация - https://lab.karpov.courses/learning/355/module/3437/lesson/30467/85657/401566/

import operator
import argparse

from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.sql import SparkSession
from pyspark.ml.classification import DecisionTreeClassifier, LogisticRegression
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.classification import GBTClassifier

MODEL_PATH = 'spark_ml_model'
LABEL_COL = 'is_bot'


def process(spark, data_path, model_path):
    """
    Основной процесс задачи.

    :param spark: SparkSession
    :param data_path: путь до датасета
    :param model_path: путь сохранения обученной модели
    """
    session_df = spark.read.parquet(data_path)

    # feature_vector = prapare_vector(session_df)
    #(training_data, test_data) = feature_vector.randomSplit([0.8, 0.2],seed = 42)

    #evaluator = MulticlassClassificationEvaluator(labelCol="is_bot", predictionCol="prediction", metricName="accuracy")

    user_type_index = StringIndexer(inputCol='user_type', outputCol='user_type_index')
    platform_index = StringIndexer(inputCol='platform', outputCol='platform_index')

    features = ['user_type_index', 'duration', 'platform_index', 'item_info_events', 'select_item_events', 'make_order_events', 'events_per_min']
    feature = VectorAssembler(inputCols=features, outputCol="features")

    dtc_classifier = DecisionTreeClassifier(labelCol="is_bot", featuresCol="features")
    pipeline = Pipeline(stages=[user_type_index, platform_index, feature, dtc_classifier])

    dtc_model = pipeline.fit(session_df)

    # lr_prediction = lr_model.transform(test_data)
    # lr_accuracy = evaluator.evaluate(lr_prediction)
    # print("LogisticRegression [Accuracy] = %g"% (lr_accuracy))
    # print("LogisticRegression [Error] = %g " % (1.0 - lr_accuracy))

    dtc_model.write().overwrite().save(model_path)


def prapare_vector(input_df):
    user_type_index = StringIndexer(inputCol='user_type', outputCol='user_type_index')
    platform_index = StringIndexer(inputCol='platform', outputCol='platform_index')

    input_df = user_type_index.fit(input_df).transform(input_df)
    input_df = platform_index.fit(input_df).transform(input_df)

    features = ['user_type_index', 'duration', 'platform_index', 'item_info_events', 'select_item_events', 'make_order_events', 'events_per_min']
    feature = VectorAssembler(inputCols=features, outputCol="features")


    feature_vector = feature.transform(input_df)

    feature_vector.show(15, truncate=0)

    return feature_vector

def main(data_path, model_path):
    spark = _spark_session()
    process(spark, data_path, model_path)


def _spark_session():
    """
    Создание SparkSession.

    :return: SparkSession
    """
    return SparkSession.builder.appName('PySparkMLFitJob').getOrCreate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='session-stat.parquet', help='Please set datasets path.')
    parser.add_argument('--model_path', type=str, default=MODEL_PATH, help='Please set model path.')
    args = parser.parse_args()
    data_path = args.data_path
    model_path = args.model_path
    main(data_path, model_path)
