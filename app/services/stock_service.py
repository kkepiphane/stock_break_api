from app.repositories.stock_repository import StockRepository
from app.services.notification_service import NotificationService

class StockService:
    def __init__(self, repo: StockRepository, notifier: NotificationService):
        self.repo = repo
        self.notifier = notifier

    async def update_stock(self, product_id: int, new_quantity: int):
        product = await self.repo.update_quantity(product_id, new_quantity)
        if product.quantity < product.min_threshold:
            await self.notifier.notify_stock_break(product)
        return product
