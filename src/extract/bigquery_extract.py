# Extract step: reads from bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022
# into a Spark DataFrame using the BigQuery Storage Read API connector.
from config.spark_config import get_spark_session


def read_table():

    spark = get_spark_session()

    df = spark.read\
        .format("bigquery")\
        .option("table", "bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022")\
        .load()
    
    return df

if __name__ == "__main__":
    print(read_table().show(10))