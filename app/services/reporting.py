from sqlalchemy.orm import Session
from app.reporting.strategies import ReportStrategy
from app.reporting.generators import ReportGenerator

class ReportingService:
    def __init__(self, db: Session, strategy: ReportStrategy):
        self.db = db
        self.strategy = strategy

    def get_report_data(self):
        return self.strategy.generate(self.db)

    def generate_report_file(self, generator: ReportGenerator) -> str:
        data = self.get_report_data()
        return generator.generate_file(data)
