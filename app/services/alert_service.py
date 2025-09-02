from typing import List
from sqlalchemy.orm import Session
from app.repositories.alert_repository import AlertRepository

class AlertService:
    def __init__(self, db: Session):
        self.repository = AlertRepository(db)

    def get_active_alerts(self):
        return self.repository.get_active_alerts()

    def get_alerts_by_product(self, product_id: int):
        return self.repository.get_alerts_by_product(product_id)

    def resolve_alert(self, alert_id: int):
        return self.repository.resolve_alert(alert_id)

    def get_alerts_stats(self):
        active_alerts = self.repository.get_active_alerts()
        stats = {
            "total_active": len(active_alerts),
            "rupture_count": len([a for a in active_alerts if a.alert_type == "rupture"]),
            "threshold_count": len([a for a in active_alerts if a.alert_type == "seuil critique"])
        }
        return stats