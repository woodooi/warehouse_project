from sqlalchemy.orm import Session
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def create_product(self, product: ProductCreate):
        # Business logic: Check if SKU exists?
        # For now, repository handles db constraints, but we could add checks here
        return self.repository.create(product)

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)
        
    def get_product_by_sku(self, sku: str):
        return self.repository.get_by_sku(sku)

    def get_products(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)

    def update_product(self, product_id: int, product_update: ProductUpdate):
        db_product = self.repository.get_by_id(product_id)
        if db_product:
            return self.repository.update(db_product, product_update)
        return None

    def delete_product(self, product_id: int):
        return self.repository.delete(product_id)
