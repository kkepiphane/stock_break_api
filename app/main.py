from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import stock

app = FastAPI(title=settings.app_name)

app.include_router(stock.router, prefix="/api/v1/stock", tags=["Stock"])
