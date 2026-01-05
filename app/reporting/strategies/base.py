from abc import ABC, abstractmethod
from typing import Any, Dict
from sqlalchemy.orm import Session
import datetime

class ReportStrategy(ABC):
    @abstractmethod
    def generate(self, db: Session, date: datetime.date) -> Dict[str, Any]:
        pass
