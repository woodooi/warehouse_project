from fastapi import FastAPI
from app.database import engine
from app.models import base
from app.schemas.transaction import TransactionRequest, TransactionType
from app.commands import ArrivalCommand, ShipmentCommand, WriteOffCommand
from app.services.warehouse import WarehouseService
from app.services.reporting import ReportingService
from app.reporting.strategies import CurrentValueStrategy, HistoricalMovementStrategy
from app.reporting.generators import InvoiceGenerator, ActGenerator
from app.observers.stock_monitor import StockMonitor
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Query
from enum import Enum

# Create tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warehouse Management System")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Warehouse Management System API"}

@app.post("/transactions")
def create_transaction(transaction: TransactionRequest, db: Session = Depends(get_db)):
    warehouse_service = WarehouseService(db)
    warehouse_service.attach(StockMonitor())

    command = None
    if transaction.type == TransactionType.ARRIVAL:
        command = ArrivalCommand(db, transaction.product_id, transaction.quantity)
    elif transaction.type == TransactionType.SHIPMENT:
        command = ShipmentCommand(db, transaction.product_id, transaction.quantity)
    elif transaction.type == TransactionType.WRITE_OFF:
        command = WriteOffCommand(db, transaction.product_id, transaction.quantity)
    
    if command:
        try:
            warehouse_service.process_transaction(command)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "Transaction executed successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

class ReportType(str, Enum):
    VALUE = "value"
    HISTORY = "history"

class ReportFormat(str, Enum):
    JSON = "json"
    INVOICE = "invoice"
    ACT = "act"

@app.get("/reports")
def get_report(
    type: ReportType, 
    format: ReportFormat = ReportFormat.JSON, 
    db: Session = Depends(get_db)
):
    strategy = None
    if type == ReportType.VALUE:
        strategy = CurrentValueStrategy()
    elif type == ReportType.HISTORY:
        strategy = HistoricalMovementStrategy()
    
    service = ReportingService(db, strategy)

    if format == ReportFormat.JSON:
        return service.get_report_data()
    
    generator = None
    if format == ReportFormat.INVOICE:
        generator = InvoiceGenerator()
    elif format == ReportFormat.ACT:
        generator = ActGenerator()
    
    if generator:
        report_content = service.generate_report_file(generator)
        return {"content": report_content}
    
    return {"error": "Invalid format"}


