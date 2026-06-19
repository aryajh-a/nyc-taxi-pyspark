# PySpark transformation functions.
# Cleans, casts, and enriches the raw taxi DataFrame before writing to GCS.
from src.extract.bigquery_extract import read_table
from pyspark.sql.functions import unix_timestamp, to_date, hour, filter, avg, sum, count, ceil, col
from src.transform.schema import REQUIRED_COLUMNS, OUTPUT_COLUMNS
import logging

logger = logging.getLogger(__name__)


def transform():
    df = read_table()

    # 1. Drop rows with null values in any of the required columns
    df_clean = df.dropna(subset = REQUIRED_COLUMNS)
    logger.info("rows with null vlues dropped")
    
    # 2. Calculate derived fields
    df_clean= df_clean.withColumn(
        "trip_duration_minutes",
        (unix_timestamp("dropoff_datetime") - unix_timestamp("pickup_datetime"))/60 
    )
    df_clean=df_clean.withColumn(
        "pickup_date",
        to_date("pickup_datetime")
    )
    df_clean=df_clean.withColumn(
        "pickup_hour",
        hour("pickup_datetime")
    )
    logger.info("derived fields calculated")

    # 3. drop impossible trips (where trip minutes is <=0)
    df_clean = df_clean.filter(df_clean["trip_duration_minutes"]>0)
    
    # 4. calculating average values per hour in a day
    df_avg = df_clean.groupBy(["pickup_date", "pickup_hour"]).agg(
        count("trip_duration_minutes").alias("total_trips"),
        avg("trip_duration_minutes").alias("average_trip_duration_minutes"),
        avg("trip_distance").alias("average_trip_distance"),
        avg("fare_amount").alias("average_fare_amount"),
        sum("fare_amount").alias("total_revenue")
    )
    logger.info("average fields calculated")

    # 5. rounding up columns to 2 digits
    for col_name in ["average_trip_duration_minutes", "average_trip_distance", "average_fare_amount"]:
        df_avg = df_avg.withColumn(col_name, ceil(col(col_name)*100)/100)
    logger.info("rounnded upto 2 decimal places")

    # Returning only the required columns
    df_final = df_avg[OUTPUT_COLUMNS]
    return df_final
    

if __name__=="__main__":
    print(transform().show(10))