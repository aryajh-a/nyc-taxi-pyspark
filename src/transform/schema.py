# StructType schema definition for tlc_yellow_trips_2022.
# Used to enforce and validate column types at ingestion time.
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
