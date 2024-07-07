# шаблон для процесса применения вашей модели, задача должна загружать вашу модель, применять ее к указанному датасету и сохранять результат предсказаний в parquet формат содержащий всего две колонки - [session_id, prediction].
#
# Параметры запуска задачи:
# data_path - путь к файлу с данными (тестовый датасет)
# model_path - путь откуда будет загружена модель
# result_path - путь куда будет сохранен результат предсказаний
# Строка запуска:

# python PySparkMLPredict.py --data_path=test.parquet --model_path=spark_ml_model --result_path=result
# ИЛИ
# spark-submit PySparkMLPredict.py --data_path=test.parquet --model_path=spark_ml_model --result_path=result

import argparse

from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession

MODEL_PATH = 'spark_ml_model'


def main(data_path, model_path, result_path):
    """
    Применение сохраненной модели.

    :param data_path: путь к файлу с данными к которым нужно сделать предсказание.
    :param model_path: путь к сохраненой модели (Из задачи PySparkMLFit.py).
    :param result_path: путь куда нужно сохранить результаты предсказаний ([session_id, prediction]).
    """
    spark = _spark_session()
    #TODO Ваш код.

    model = PipelineModel.read().load(model_path)
    prediction = model.transform(spark.read.parquet(data_path))
    prediction.select('session_id', 'prediction').write.save(result_path)

def _spark_session():
    """
    Создание SparkSession.

    :return: SparkSession
    """
    return SparkSession.builder.appName('PySparkMLPredict').getOrCreate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default=MODEL_PATH, help='Please set model path.')
    parser.add_argument('--data_path', type=str, default='test.parquet', help='Please set datasets path.')
    parser.add_argument('--result_path', type=str, default='result', help='Please set result path.')
    args = parser.parse_args()
    data_path = args.data_path
    model_path = args.model_path
    result_path = args.result_path
    main(data_path, model_path, result_path)
