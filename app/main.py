from fastapi import FastAPI
from app.core.config import settings
from app.api import stock

app = FastAPI(title=settings.app_name)

app.include_router(stock.router, prefix="/api/stock", tags=["Stock"])
