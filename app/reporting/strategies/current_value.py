from .base import ReportStrategy
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from typing import Dict, Any

class CurrentValueStrategy(ReportStrategy):
    def generate(self, db: Session) -> Dict[str, Any]:
        products = db.query(Product).all()
        total_value = sum(p.quantity * p.price for p in products)
        product_details = [
            {"id": p.id, "name": p.name, "quantity": p.quantity, "price": p.price, "value": p.quantity * p.price}
            for p in products
        ]
        return {
            "report_type": "Current Inventory Value",
            "total_value": total_value,
            "details": product_details
        }
