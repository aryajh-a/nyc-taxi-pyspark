# Load step: writes the transformed DataFrame to GCS as date-partitioned Parquet.
# Uses partitionBy("pickup_date") for query pruning and idempotent overwrites.
from src.transform.transforms import transform
from src.transform.schema import TRANSFORMED_SCHEMA
import logging

logger = logging.getLogger(__name__)
                 
def load():
    df = transform()

    # schema validation
    schema_validation(df)

    # load locally
    df.write\
        .format("parquet")\
        .mode("overwrite")\
        .partitionBy("pickup_date")\
        .save("output/data")

    return True

def schema_validation(df):
    actual = {col.name:col.dataType for col in df.schema.fields}
    expected = {col.name:col.dataType for col in TRANSFORMED_SCHEMA.fields }

    if actual!=expected:
        raise ValueError(f"Schema mismatch. \nExpected: {expected}\nActual: {actual}")
    logger.info("Schema validated!!")

if __name__=="__main__":
    print(load())