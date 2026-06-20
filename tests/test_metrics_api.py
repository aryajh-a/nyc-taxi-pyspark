import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_daily_metrics_valid_date():
    response = client.get("/metrics/daily?pickup_date=2022-01-15")
    assert response.status_code == 200
    data = response.json()
    assert data["pickup_date"] == "2022-01-15"
    assert data["total_trips"] > 0
    assert "average_fare_amount" in data
    assert "average_trip_distance" in data
    assert "average_trip_duration_minutes" in data

def test_daily_metrics_missing_date():
    response = client.get("/metrics/daily?pickup_date=1800-01-01")
    assert response.status_code == 404

def test_daily_metrics_invalid_format():
    response = client.get("/metrics/daily?pickup_date=not-a-date")
    assert response.status_code == 422

def test_summary_returns_records():
    response = client.get("/metrics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "records" in data
    assert "total_dates" in data
    assert data["total_dates"] == len(data["records"])
    assert data["total_dates"] > 0

def test_summary_record_schema():
    response = client.get("/metrics/summary")
    assert response.status_code == 200
    record = response.json()["records"][0]
    assert "pickup_date" in record
    assert "total_trips" in record
    assert "total_revenue" in record
