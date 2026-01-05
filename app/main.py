from fastapi import FastAPI
from app.database import engine
from app.models import base
from app.schemas.transaction import TransactionRequest, TransactionType
from app.commands import ArrivalCommand, ShipmentCommand, WriteOffCommand
from app.services.warehouse import WarehouseService
from app.services.reporting import ReportingService
from app.reporting.strategies import CurrentValueStrategy, HistoricalMovementStrategy, StateStrategy
from app.reporting.generators import InvoiceGenerator, ActGenerator
from app.observers.stock_monitor import StockMonitor
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from enum import Enum
from app.services.product import ProductService
from app.schemas.product import Product, ProductCreate
from app.services.supplier import SupplierService
from app.schemas.supplier import Supplier, SupplierCreate
import datetime
from typing import Optional

# Create tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warehouse Management System")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/products", response_model=list[Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.get_products(skip, limit)

@app.post("/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.create_product(product)

@app.get("/suppliers", response_model=list[Supplier])
def get_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    supplier_service = SupplierService(db)
    return supplier_service.get_suppliers(skip, limit)

@app.post("/suppliers", response_model=Supplier)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    supplier_service = SupplierService(db)
    return supplier_service.create_supplier(supplier)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Warehouse Management System API. Visit /static/index.html for the dashboard."}

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
    STATE = "state"

class ReportFormat(str, Enum):
    JSON = "json"
    INVOICE = "invoice"
    ACT = "act"

@app.get("/reports")
def get_report(
    type: ReportType, 
    format: ReportFormat = ReportFormat.JSON, 
    date: Optional[datetime.date] = None,
    db: Session = Depends(get_db)
):
    strategy = None
    if type == ReportType.VALUE:
        strategy = CurrentValueStrategy()
    elif type == ReportType.HISTORY:
        strategy = HistoricalMovementStrategy()
    elif type == ReportType.STATE:
        strategy = StateStrategy()
    service = ReportingService(db, strategy)

    if format == ReportFormat.JSON:
        return service.get_report_data(date)
    
    generator = None
    if format == ReportFormat.INVOICE:
        generator = InvoiceGenerator()
    elif format == ReportFormat.ACT:
        generator = ActGenerator()
    
    if generator:
        report_content = service.generate_report_file(generator, date)
        return {"content": report_content}
    
    return {"error": "Invalid format"}


