from sqlalchemy.orm import Session
from .base import BaseRepository
from app.models.transaction import TransactionHistory
from datetime import datetime, time

class TransactionRepository(BaseRepository[TransactionHistory]):
    def __init__(self, db: Session):
        super().__init__(db, TransactionHistory)

    def get_by_date(self, target_date):
        # Перетворюємо дату (date) у кінець дня (datetime: 23:59:59)
        end_of_day = datetime.combine(target_date, time.max) 
        
        return self.db.query(TransactionHistory).filter(
            TransactionHistory.timestamp > end_of_day
    ).all()
