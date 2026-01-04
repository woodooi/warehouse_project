from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_email = Column(String(255))
    
    products = relationship("Product", back_populates="supplier")
