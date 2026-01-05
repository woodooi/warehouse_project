from .base import ReportStrategy
import datetime
from sqlalchemy.orm import Session
from app.models.transaction import TransactionHistory
from app.repositories.transaction import TransactionRepository
from sqlalchemy import func
from typing import Dict, Any

class HistoricalMovementStrategy(ReportStrategy):
    def generate(self, db: Session, date: datetime.date) -> Dict[str, Any]:
        transactions = TransactionRepository(db).get_by_date(date)
        # Simply aggregating counts for demo purposes
        movement_summary = {
            "ARRIVAL": 0,
            "SHIPMENT": 0,
            "WRITE_OFF": 0
        }
        for t in transactions:
            if t.type in movement_summary:
                movement_summary[t.type] += t.quantity
        
        return {
            "report_type": "Historical Stock Movement",
            "summary": movement_summary,
            "total_transactions": len(transactions)
        }
