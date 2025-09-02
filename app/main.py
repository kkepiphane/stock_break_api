from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import auth, users, products, stock_movements, alerts
from app.startup import wait_for_postgres, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Stock Management API...")
    if wait_for_postgres():
        init_db()
    else:
        logger.error("Failed to connect to database. Exiting...")
        raise RuntimeError("Database connection failed")
    yield
    # Shutdown
    logger.info("🛑 Shutting down Stock Management API...")

app = FastAPI(
    title="Stock Management API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(stock_movements.router)
app.include_router(alerts.router)

@app.get("/")
async def root():
    return {"message": "Stock Management API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}