# Load step: writes the transformed DataFrame to GCS as date-partitioned Parquet.
# Uses partitionBy("pickup_date") for query pruning and idempotent overwrites.
