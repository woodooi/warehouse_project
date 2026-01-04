from fastapi import FastAPI
from app.database import engine
from app.models import base

# Create tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warehouse Management System")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Warehouse Management System API"}
