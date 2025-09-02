from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, users, products, stock_movements, alerts

app = FastAPI(title="Stock Management API", version="1.0.0")

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
    return {"status": "healthy"}