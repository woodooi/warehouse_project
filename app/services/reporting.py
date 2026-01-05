from sqlalchemy.orm import Session
from app.reporting.strategies import ReportStrategy
from app.reporting.generators import ReportGenerator
import datetime

class ReportingService:
    def __init__(self, db: Session, strategy: ReportStrategy):
        self.db = db
        self.strategy = strategy

    def get_report_data(self, date: datetime.date = None):
        if date is None:
            date = datetime.date.today()
        return self.strategy.generate(self.db, date)

    def generate_report_file(self, generator: ReportGenerator, date: datetime.date = None) -> str:
        if date is None:
            date = datetime.date.today()
        data = self.get_report_data(date)
        return generator.generate_file(data, date)
