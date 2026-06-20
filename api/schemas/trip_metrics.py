# Pydantic response models for the metrics endpoints.
# Defines the shape of the JSON response using Pydantic
from pydantic import BaseModel
from datetime import date

class TripMetrics(BaseModel):
    pickup_date: date
    total_trips: int
    average_fare_amount: float
    average_trip_distance: float
    average_trip_duration_minutes: float

class DailySummaryItem(BaseModel):
    pickup_date: date
    total_trips: int
    total_revenue: float

class SummaryResponse(BaseModel):
    records: list[DailySummaryItem]
    total_dates: int
