# FastAPI application entry point.
# Mounts routers and configures the app instance.
from fastapi import FastAPI
from api.routers.metrics import router as metrics_router

# create app
app = FastAPI()

# include routers from metrics.py
app.include_router(metrics_router)


@app.get("/")
async def root():
    return {"message":"Main application root"}