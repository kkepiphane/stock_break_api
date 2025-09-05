from pydantic import BaseModel
from datetime import datetime

# ----- Sorties -----
class AlertOut(BaseModel):
    id: int
    product_id: int
    alert_type: str
    is_resolved: bool
    created_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True
