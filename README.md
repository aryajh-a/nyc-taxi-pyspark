# NYC Taxi PySpark ETL Pipeline

A data engineering portfolio project using the NYC Yellow Taxi public dataset.

**Source:** `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`

## Pipeline

```
BigQuery Public Dataset
        ↓
PySpark (schema validation + transforms + partitioned Parquet writes)
        ↓
Local Parquet (date-partitioned, output/data/)
        ↓
FastAPI (REST endpoints serving metrics from Parquet)
```

## Stack

| Component     | Role                                      |
|---------------|-------------------------------------------|
| PySpark       | Schema validation, transformation, writes |
| Local Parquet | Date-partitioned staging layer            |
| FastAPI       | REST API serving aggregated metrics       |
| Pydantic      | Response model validation                 |
| pandas        | Parquet reads inside the API layer        |

## Repo Structure

```
nyc-taxi-pyspark/
├── config/
│   └── spark_config.py          # SparkSession builder
├── src/
│   ├── extract/
│   │   └── bigquery_extract.py  # Read from BQ public dataset
│   ├── transform/
│   │   ├── schema.py            # StructType schema + column lists
│   │   └── transforms.py        # PySpark transformation functions
│   └── load/
│       └── load.py              # Schema validation + partitioned Parquet write
├── api/
│   ├── main.py                  # FastAPI app entry point
│   ├── routers/
│   │   └── metrics.py           # /metrics route handlers
│   └── schemas/
│       └── trip_metrics.py      # Pydantic response models
├── tests/
│   └── test_metrics_api.py      # API endpoint tests
└── requirements.txt
```

---

## Running the ETL

```bash
python -m src.load.load
```

Output written to `output/data/pickup_date=YYYY-MM-DD/`.

---

## Running the API

```bash
uvicorn api.main:app --reload
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/metrics/daily?pickup_date=2022-01-15` | Aggregated metrics for a single date |
| GET | `/metrics/summary` | Trip counts and revenue across all dates |

- Returns `404` if the requested date has no data
- Swagger UI available at `http://localhost:8000/docs`

---

## Running Tests

```bash
pytest tests/test_metrics_api.py -v
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

**Exit criteria:** `pyspark` launches in the terminal, Spark UI loads at `localhost:4040`.

---

### Phase 1 — SparkSession Config (`config/spark_config.py`)
**Goal:** A reusable function that returns a configured SparkSession with the BigQuery connector wired in.

Tasks:
- Configure BigQuery Storage Read API connector JAR
- Set GCS temp bucket for BQ reads
- Set GCP credentials path

**Exit criteria:** `get_spark_session()` returns a live SparkSession with no import errors.

---

### Phase 2 — Extract (`src/extract/bigquery_extract.py`)
**Goal:** Read the BQ public table into a Spark DataFrame.

Tasks:
- Use the SparkSession from Phase 1
- Read `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`

**Exit criteria:** DataFrame with correct columns and non-zero row count.

---

### Phase 3 — Schema + Transform (`src/transform/`)
**Goal:** Enforce schema at ingestion, clean and enrich the DataFrame.

Tasks:
- Define `StructType` schema matching BQ table columns
- Drop nulls in required columns, filter zero-duration trips
- Add derived columns: `pickup_date`, `pickup_hour`, `trip_duration_minutes`
- Aggregate per `(pickup_date, pickup_hour)`: trip count, avg fare, avg distance, total revenue
- Round decimal columns to 2 places

**Exit criteria:** Transformed DataFrame has correct columns, types, and no invalid rows.

---

### Phase 4 — Load (`src/load/load.py`)
**Goal:** Write the transformed DataFrame to local disk as date-partitioned Parquet.

Tasks:
- Validate output schema against `TRANSFORMED_SCHEMA` before writing
- Write with `partitionBy("pickup_date")` and `mode("overwrite")`
- Target path: `output/data/`

**Exit criteria:** `output/data/` contains `pickup_date=YYYY-MM-DD/` folders with Parquet files.

---

### Phase 5 — FastAPI (`api/`)
**Goal:** REST API serving aggregated metrics read directly from local Parquet.

Tasks:
- `GET /metrics/daily?pickup_date=YYYY-MM-DD` — per-hour rows aggregated to a single daily response
- `GET /metrics/summary` — all dates with total trips and revenue
- Pydantic response models in `schemas/trip_metrics.py`
- 404 for missing dates

**Exit criteria:** Both endpoints return correct JSON; Swagger UI at `/docs` works; API tests pass.

---

## Related Project

[nyc-taxi-etl-airflow](https://github.com/aryajh-a/nyc-taxi-etl-airflow-) — same dataset, pandas-based transformation, built first.
