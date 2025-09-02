from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.alert import Alert
from app.repositories.product_repository import ProductRepository
from app.repositories.alert_repository import AlertRepository
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: Session):
        self.product_repo = ProductRepository(db)
        self.alert_repo = AlertRepository(db)

    def create_product(self, product_create: ProductCreate) -> Product:
        # Vérifier si le SKU existe déjà
        if self.product_repo.get_by_sku(product_create.sku):
            raise ValueError("SKU already exists")
        
        product = self.product_repo.create(product_create.dict())
        
        # Vérifier les alertes après création
        self._check_stock_alerts(product)
        
        return product

    def update_product(self, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
        product = self.product_repo.get_by_id(product_id)
        if product:
            update_data = product_update.dict(exclude_unset=True)
            product = self.product_repo.update(product, update_data)
            
            # Vérifier les alertes après mise à jour
            self._check_stock_alerts(product)
            
            return product
        return None

    def get_low_stock_products(self, threshold: int = None) -> List[Product]:
        return self.product_repo.get_low_stock_products(threshold)

    def _check_stock_alerts(self, product: Product):
        # Vérifier et créer des alertes si nécessaire
        if product.quantity <= 0:
            self._create_alert(product, "rupture")
        elif product.quantity <= product.min_threshold:
            self._create_alert(product, "seuil critique")

    def _create_alert(self, product: Product, alert_type: str):
        # Vérifier s'il n'y a pas déjà une alerte active du même type
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