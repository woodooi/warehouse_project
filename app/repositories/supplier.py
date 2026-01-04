from sqlalchemy.orm import Session
from .base import BaseRepository
from app.models.supplier import Supplier

class SupplierRepository(BaseRepository[Supplier]):
    def __init__(self, db: Session):
        super().__init__(db, Supplier)
