from pydantic import BaseModel
from typing import Optional, List

class SupplierBase(BaseModel):
    name: str
    contact_email: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_email: Optional[str] = None

class Supplier(SupplierBase):
    id: int
    
    class Config:
        from_attributes = True
