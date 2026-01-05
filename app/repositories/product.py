from sqlalchemy.orm import Session, joinedload
from .base import BaseRepository
from app.models.product import Product
from typing import List

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(db, Product)
    
    def get_by_sku(self, sku: str):
        return self.db.query(self._model).filter(self._model.sku == sku).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(self._model).options(joinedload(Product.supplier)).offset(skip).limit(limit).all()
