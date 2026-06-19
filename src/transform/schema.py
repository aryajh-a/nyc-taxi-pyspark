# StructType schema definition for tlc_yellow_trips_2022.
# Used to enforce and validate column types at ingestion time.
from pyspark.sql.types import StructField, StructType, DateType, IntegerType, DoubleType, LongType, DecimalType

REQUIRED_COLUMNS = [
    "pickup_datetime",
    "dropoff_datetime",
    "trip_distance",
    "fare_amount",
    "total_amount",
]

OUTPUT_COLUMNS = [
    "pickup_date",
    "pickup_hour",
    "total_trips",
    "average_trip_duration_minutes",
    "average_trip_distance",
    "average_fare_amount",
    "total_revenue",
]

TRANSFORMED_SCHEMA=StructType([
    StructField("pickup_date", DateType(), nullable=False),
    StructField("pickup_hour", IntegerType(), nullable=False),
    StructField("total_trips", LongType(), nullable=False),
    StructField("average_trip_duration_minutes", DoubleType(), nullable=False),
    StructField("average_trip_distance", DecimalType(36,6), nullable=False),
    StructField("average_fare_amount", DecimalType(36,6), nullable=False),
    StructField("total_revenue", DecimalType(38,9), nullable=False),
])