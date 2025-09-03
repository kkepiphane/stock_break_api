from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.stock_movement import StockMovement
from app.models.product import Product
from app.repositories.stock_movement_repository import StockMovementRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.alert_repository import AlertRepository
from app.schemas.stock_movement import StockMovementCreate

class StockMovementService:
    def __init__(self, db: Session):
        self.movement_repo = StockMovementRepository(db)
        self.product_repo = ProductRepository(db)
        self.alert_repo = AlertRepository(db)

    def create_movement(self, movement_create: StockMovementCreate) -> StockMovement:
        product = self.product_repo.get_by_id(movement_create.product_id)
        if not product:
            raise ValueError("Product not found")

        # Créer le mouvement de stock
        movement = self.movement_repo.create(movement_create.dict())

        # Mettre à jour la quantité du produit
        self.product_repo.update_quantity(product.id, movement_create.change)

        # Vérifier les alertes
        updated_product = self.product_repo.get_by_id(product.id)
        self._check_stock_alerts(updated_product)

        return movement

    def get_product_movements(self, product_id: int, skip: int = 0, limit: int = 100) -> List[StockMovement]:
        return self.movement_repo.get_movements_by_product(product_id, skip, limit)

    def get_recent_movements(self, days: int = 7, skip: int = 0, limit: int = 100) -> List[StockMovement]:
        return self.movement_repo.get_recent_movements(days, skip, limit)

    def _check_stock_alerts(self, product: Product):
        # Vérifier et créer des alertes si nécessaire
        if product.quantity <= 0:
            self._create_alert(product, "rupture")
        elif product.quantity <= product.min_threshold:
            self._create_alert(product, "seuil critique")
        else:
            # Résoudre les alertes si le stock est suffisant
            self._resolve_alerts(product)

    def _create_alert(self, product: Product, alert_type: str):
        existing_alerts = self.alert_repo.get_alerts_by_product(product.id)
        active_same_type = any(
            alert for alert in existing_alerts 
            if alert.alert_type == alert_type and not alert.is_resolved
        )
        
        if not active_same_type:
            alert_data = {
                "product_id": product.id,
                "alert_type": alert_type,
                "is_resolved": False
            }
            self.alert_repo.create(alert_data)

    def _resolve_alerts(self, product: Product):
        # Résoudre toutes les alertes actives pour ce produit
        active_alerts = [alert for alert in self.alert_repo.get_alerts_by_product(product.id) 
                        if not alert.is_resolved]
        
        for alert in active_alerts:
            self.alert_repo.resolve_alert(alert.id)