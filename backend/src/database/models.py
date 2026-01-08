from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WheyProteinDB(Base):
    __tablename__ = "whey_proteins"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    brand = Column(String)
    serving_size = Column(Integer)
    total_weight = Column(Integer)
    protein_per_serving = Column(Integer)
    fenilanina = Column(Float, default=0.0)
    histidina = Column(Float, default=0.0)
    isoleucina = Column(Float, default=0.0)
    leucina = Column(Float, default=0.0)
    lisina = Column(Float, default=0.0)
    metionina = Column(Float, default=0.0)
    treonina = Column(Float, default=0.0)
    triptofano = Column(Float, default=0.0)
    valina = Column(Float, default=0.0)