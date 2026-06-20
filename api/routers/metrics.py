# Router: /metrics endpoints — queries local aggregated tables and returns JSON.
from fastapi import APIRouter, HTTPException
from datetime import date
from pathlib import Path
import pandas as pd
from api.schemas.trip_metrics import TripMetrics, DailySummaryItem, SummaryResponse

router = APIRouter(prefix="/metrics", tags=["metrics"])

def load_parquet_for_date(pickup_date: date):
    file_path = Path(f"output/data/pickup_date={pickup_date}")
    # 1. Verify that the file directory exists
    if not file_path.is_dir():
        raise HTTPException(status_code=404, detail=f"No data for date : {pickup_date}")
    # 2. Read the file into a dataframe
    try:
        df = pd.read_parquet(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading the file")
    
    return df

def load_all_parquet():
    file_path = Path("output/data")
    # 1. Verify that the file directory exists
    if not file_path.is_dir():
        raise HTTPException(status_code=500, detail=f"No data found")
    # 2. Read the file into a dataframe
    try:
        df = pd.read_parquet(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading the file")
    
    return df

# Endpoint
@router.get("/daily", response_model=TripMetrics)
def get_daily_metrics(pickup_date: date):
    # get data for the particular date
    df = load_parquet_for_date(pickup_date)

    # read into variables
    total_trips = int(df["total_trips"].sum())
    average_fare_amount = float(df["average_fare_amount"].astype(float).mean())
    average_trip_distance = float(df["average_trip_distance"].astype(float).mean())
    average_trip_duration_minutes = float(df["average_trip_duration_minutes"].mean())

    
    # in correct json format as put in trip_metrics
    return TripMetrics(
        pickup_date= pickup_date,
        total_trips=total_trips,
        average_fare_amount=average_fare_amount,
        average_trip_distance=average_trip_distance,
        average_trip_duration_minutes=average_trip_duration_minutes
    )

# Endpoint
@router.get("/summary", response_model=SummaryResponse)
def get_summary():
    # reading all files
    df = load_all_parquet()
    df["total_revenue"]=df["total_revenue"].astype(float)

    df_daily = df.groupby("pickup_date").agg(
        total_trips=("total_trips","sum"),
        total_revenue=("total_revenue","sum")
    ).reset_index()

    summary_list=[]
    for row in df_daily.itertuples():
        summary_list.append(DailySummaryItem(pickup_date=row.pickup_date, 
                                             total_trips=row.total_trips, 
                                             total_revenue=row.total_revenue))

    total_dates = len(df_daily)

    return SummaryResponse(
        records=summary_list,
        total_dates=total_dates
    )
