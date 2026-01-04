from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    sku: str
    quantity: int = 0
    price: float = 0.0
    min_stock: int = 0
    supplier_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    min_stock: Optional[int] = None
    supplier_id: Optional[int] = None

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
