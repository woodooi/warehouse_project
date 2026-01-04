from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TransactionType(str, Enum):
    ARRIVAL = "ARRIVAL"
    SHIPMENT = "SHIPMENT"
    WRITE_OFF = "WRITE_OFF"

class TransactionRequest(BaseModel):
    product_id: int
    quantity: int
    type: TransactionType

class TransactionResponse(BaseModel):
    id: int
    product_id: int
    type: str
    quantity: int
    timestamp: str 

    class Config:
        from_attributes = True
