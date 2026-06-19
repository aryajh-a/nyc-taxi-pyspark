# SparkSession configuration
# Builds and returns a configured SparkSession for the NYC Taxi pipeline.
from pyspark.sql import SparkSession

def get_spark_session():
    spark = SparkSession.builder\
        .master("local[*]")\
        .appName("nyc-taxi-pyspark")\
        .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.36.1")\
        .config("spark.driver.host", "127.0.0.1")\
        .config("spark.driver.bindAddress", "127.0.0.1")\
        .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")\
        .config("spark.driver.extraJavaOptions", "-Djava.library.path=C:/hadoop/bin")\
        .getOrCreate()

    return spark