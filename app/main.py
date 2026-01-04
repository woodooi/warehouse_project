from fastapi import FastAPI
from app.database import engine
from app.models import base
from app.schemas.transaction import TransactionRequest, TransactionType
from app.commands import ArrivalCommand, ShipmentCommand, WriteOffCommand
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

# Create tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warehouse Management System")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Warehouse Management System API"}

@app.post("/transactions")
def create_transaction(transaction: TransactionRequest, db: Session = Depends(get_db)):
    command = None
    if transaction.type == TransactionType.ARRIVAL:
        command = ArrivalCommand(db, transaction.product_id, transaction.quantity)
    elif transaction.type == TransactionType.SHIPMENT:
        command = ShipmentCommand(db, transaction.product_id, transaction.quantity)
    elif transaction.type == TransactionType.WRITE_OFF:
        command = WriteOffCommand(db, transaction.product_id, transaction.quantity)
    
    if command:
        try:
            command.execute()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "Transaction executed successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

