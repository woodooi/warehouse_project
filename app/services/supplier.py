from sqlalchemy.orm import Session
from app.repositories.supplier import SupplierRepository
from app.schemas.supplier import SupplierCreate, SupplierUpdate

class SupplierService:
    def __init__(self, db: Session):
        self.repository = SupplierRepository(db)

    def create_supplier(self, supplier: SupplierCreate):
        return self.repository.create(supplier)

    def get_supplier(self, supplier_id: int):
        return self.repository.get_by_id(supplier_id)

    def get_suppliers(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)

    def update_supplier(self, supplier_id: int, supplier_update: SupplierUpdate):
        db_supplier = self.repository.get_by_id(supplier_id)
        if db_supplier:
            return self.repository.update(db_supplier, supplier_update)
        return None

    def delete_supplier(self, supplier_id: int):
        return self.repository.delete(supplier_id)
