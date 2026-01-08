from fastapi import FastAPI
from .database.database import create_tables
from .api.routes import router

app = FastAPI(title="Whey Protein API", version="1.0.0")

@app.on_event("startup")
def startup_event():
    create_tables()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Whey Protein API"}