# NYC Taxi PySpark ETL Pipeline

A data engineering portfolio project using the NYC Yellow Taxi public dataset.

**Source:** `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`

## Pipeline

```
BigQuery Public Dataset
        ↓
PySpark (StructType schema validation + transforms + partitioned Parquet writes)
        ↓
Local Parquet (date-partitioned, output/data/)
        ↓
dbt (models + tests on BigQuery)
        ↓
BigQuery (clean aggregated tables)
        ↓
FastAPI (REST endpoints serving metrics)
```

## Stack

| Component   | Role                                      |
|-------------|-------------------------------------------|
| PySpark     | Schema validation, transformation, writes |
| Local Parquet | Parquet staging layer (output/data/)    |
| dbt         | Final transformation + testing on BQ      |
| BigQuery    | Aggregated serving tables                 |
| FastAPI     | REST API serving metrics                  |
| Airflow     | Orchestration                             |

## Repo Structure

```
nyc-taxi-pyspark/
├── config/
│   └── spark_config.py          # SparkSession builder
├── src/
│   ├── extract/
│   │   └── bigquery_extract.py  # Read from BQ public dataset
│   ├── transform/
│   │   ├── schema.py            # StructType schema definition
│   │   └── transforms.py        # PySpark transformation functions
│   └── load/
│       └── load.py              # Partitioned Parquet write to local disk
├── dbt/
│   ├── models/
│   │   ├── staging/             # stg_yellow_trips.sql
│   │   └── marts/               # agg_trips_by_date.sql
│   └── tests/
├── api/
│   ├── main.py                  # FastAPI app
│   ├── routers/metrics.py       # /metrics endpoints
│   └── schemas/trip_metrics.py  # Pydantic response models
├── dags/
│   └── nyc_taxi_pipeline.py     # Airflow DAG
└── tests/
    ├── test_extract.py
    ├── test_transforms.py
    └── test_load.py
```

---

## Phase Plan

### Phase 0 — Environment Setup
**Goal:** Working local Spark environment on Windows.

Tasks:
- Install JDK 17, set `JAVA_HOME`
- Install winutils.exe, set `HADOOP_HOME`
- Create Python 3.11 virtual environment
- `pip install -r requirements.txt`
- Verify: `pyspark` shell starts without errors

**Exit criteria:** `pyspark` launches in the terminal, Spark UI loads at `localhost:4040`.

---

### Phase 1 — SparkSession Config (`config/spark_config.py`)
**Goal:** A reusable function that returns a configured SparkSession with the BigQuery connector wired in.

Tasks:
- Configure BigQuery Storage Read API connector JAR
- Set GCS temp bucket for BQ reads
- Set GCP credentials path

**Exit criteria:** `get_spark_session()` returns a live SparkSession; no import errors.

---

### Phase 2 — Extract (`src/extract/bigquery_extract.py`)
**Goal:** Read the BQ public table into a Spark DataFrame.

Tasks:
- Use the SparkSession from Phase 1
- Read `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`
- Print schema and row count to confirm data loads

**Exit criteria:** DataFrame with correct columns and non-zero row count printed to console.

---

### Phase 3 — Schema + Transform (`src/transform/schema.py` + `transforms.py`)
**Goal:** Enforce schema at ingestion, clean and enrich the DataFrame.

Tasks:
- Define `StructType` schema matching BQ table columns
- Apply schema to raw DataFrame (reject or flag bad rows)
- Add derived column: `pickup_date` (cast from `tpep_pickup_datetime`)
- Drop nulls in key columns, filter invalid fares/distances
- Write unit tests in `tests/test_transforms.py`

**Exit criteria:** Transformed DataFrame passes all unit tests; `pickup_date` column present and correctly typed.

---

### Phase 4 — Load (`src/load/load.py`)
**Goal:** Write the transformed DataFrame to local disk as date-partitioned Parquet.

Tasks:
- Write with `partitionBy("pickup_date")`
- Use `mode("overwrite")` for idempotency
- Target path: `output/data/`
- Validate output schema against `TRANSFORMED_SCHEMA` before writing

**Exit criteria:** `output/data/` contains `pickup_date=YYYY-MM-DD/` folders with Parquet files; re-running overwrites cleanly.

---

### Phase 5 — dbt (`dbt/`)
**Goal:** Transform the GCS-loaded data in BigQuery using dbt models with tests.

Tasks:
- `dbt init` inside `dbt/` directory
- Configure `profiles.yml` for BigQuery
- Write `stg_yellow_trips.sql` staging model
- Write `agg_trips_by_date.sql` mart model (daily trip count, avg fare, avg distance)
- Add `not_null` and `unique` dbt tests
- `dbt run` + `dbt test` pass

**Exit criteria:** `dbt run` and `dbt test` both pass; aggregated table exists in BigQuery.

---

### Phase 6 — FastAPI (`api/`)
**Goal:** REST API serving aggregated metrics from BigQuery.

Tasks:
- `GET /metrics/daily` — returns daily trip stats from the mart model
- `GET /metrics/daily/{date}` — returns stats for a specific date
- Pydantic response models in `schemas/trip_metrics.py`
- Manual test with `uvicorn` + browser/curl

**Exit criteria:** Both endpoints return correct JSON; Swagger UI at `/docs` works.

---

### Phase 7 — Airflow Orchestration (`dags/nyc_taxi_pipeline.py`)
**Goal:** Full pipeline runs end-to-end on a schedule via Airflow.

Tasks:
- Define DAG with tasks: extract → transform → load → dbt run → dbt test
- Pass GCS URIs between tasks (XCom or task arguments)
- Add email alerting on failure
- Trigger DAG manually, confirm all tasks go green

**Exit criteria:** Full DAG run succeeds end-to-end in Airflow UI with all tasks green.

---

## Related Project

[nyc-taxi-etl-airflow](https://github.com/aryajh-a/nyc-taxi-etl-airflow-) — same dataset, pandas-based transformation, built first.
