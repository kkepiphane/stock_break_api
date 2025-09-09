from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_alert_service
from app.schemas.alert import AlertOut
from app.services.alert_service import AlertService
from app.dependencies import get_current_user

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=List[AlertOut])
async def get_all_alerts(
    skip: int = 0,
    limit: int = 100,
    alert_service: AlertService = Depends(get_alert_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user.role not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    alerts = alert_service.repository.get_all(skip, limit)
    return alerts

@router.get("/active/", response_model=List[AlertOut])
async def get_active_alerts(
    alert_service: AlertService = Depends(get_alert_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user.role not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    alerts = alert_service.get_active_alerts()
    return alerts

@router.get("/stats/")
async def get_alerts_stats(
    alert_service: AlertService = Depends(get_alert_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user.role not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    stats = alert_service.get_alerts_stats()
    return stats

@router.get("/product/{product_id}", response_model=List[AlertOut])
async def get_product_alerts(
    product_id: int,
    alert_service: AlertService = Depends(get_alert_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user.role not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    alerts = alert_service.get_alerts_by_product(product_id)
    return alerts

@router.patch("/{alert_id}/resolve", response_model=AlertOut)
async def resolve_alert(
    alert_id: int,
    alert_service: AlertService = Depends(get_alert_service),
    current_user: dict = Depends(get_current_user)
):
    if current_user.role not in ["admin", "commercial"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    alert = alert_service.resolve_alert(alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    return alert