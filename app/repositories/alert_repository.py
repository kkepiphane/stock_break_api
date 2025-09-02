from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.alert import Alert
from app.repositories.base import BaseRepository

class AlertRepository(BaseRepository[Alert]):
    def __init__(self, db: Session):
        super().__init__(Alert, db)

    def get_active_alerts(self):
        return self.db.query(Alert).filter(Alert.is_resolved == False).all()

    def get_alerts_by_product(self, product_id: int):
        return (
            self.db.query(Alert)
            .filter(Alert.product_id == product_id)
            .order_by(desc(Alert.created_at))
            .all()
        )

    def resolve_alert(self, alert_id: int):
        alert = self.get_by_id(alert_id)
        if alert and not alert.is_resolved:
            alert.is_resolved = True
            alert.resolved_at = func.now()
            self.db.commit()
            self.db.refresh(alert)
        return alert