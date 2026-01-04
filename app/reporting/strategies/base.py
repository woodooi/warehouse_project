from abc import ABC, abstractmethod
from typing import Any, Dict
from sqlalchemy.orm import Session

class ReportStrategy(ABC):
    @abstractmethod
    def generate(self, db: Session) -> Dict[str, Any]:
        pass
