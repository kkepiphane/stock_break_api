from sqlalchemy.orm import Session
from app.models.product import Product
from app.repositories.base import BaseRepository

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(Product, db)

    def get_by_sku(self, sku: str):
        return self.db.query(Product).filter(Product.sku == sku).first()

    def get_low_stock_products(self, threshold: int = None):
        query = self.db.query(Product)
        if threshold is not None:
            query = query.filter(Product.quantity <= threshold)
        else:
            query = query.filter(Product.quantity <= Product.min_threshold)
        return query.all()

    def update_quantity(self, product_id: int, change: int):
        product = self.get_by_id(product_id)
        if product:
            product.quantity += change
            self.db.commit()
            self.db.refresh(product)
        return product