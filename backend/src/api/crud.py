from sqlalchemy.orm import Session
from typing import List
from ..database.models import WheyProteinDB
from ..api.schemas import WheyProteinCreate

def create_whey_protein(db: Session, whey_protein: WheyProteinCreate) -> WheyProteinDB:
    db_whey_protein = WheyProteinDB(**whey_protein.dict())
    db.add(db_whey_protein)
    db.commit()
    db.refresh(db_whey_protein)
    return db_whey_protein

def get_whey_protein(db: Session, whey_protein_id: int) -> WheyProteinDB:
    return db.query(WheyProteinDB).filter(WheyProteinDB.id == whey_protein_id).first()

def get_whey_proteins(db: Session, skip: int = 0, limit: int = 100) -> List[WheyProteinDB]:
    return db.query(WheyProteinDB).offset(skip).limit(limit).all()

def update_whey_protein(db: Session, whey_protein_id: int, whey_protein: WheyProteinCreate) -> WheyProteinDB:
    db_whey_protein = db.query(WheyProteinDB).filter(WheyProteinDB.id == whey_protein_id).first()
    if db_whey_protein:
        for key, value in whey_protein.dict().items():
            setattr(db_whey_protein, key, value)
        db.commit()
        db.refresh(db_whey_protein)
    return db_whey_protein

def delete_whey_protein(db: Session, whey_protein_id: int) -> bool:
    db_whey_protein = db.query(WheyProteinDB).filter(WheyProteinDB.id == whey_protein_id).first()
    if db_whey_protein:
        db.delete(db_whey_protein)
        db.commit()
        return True
    return False