from sqlalchemy.orm import Session
from typing import List
from ..database.models import WheyProteinDB, BrandDB
from ..api.schemas import WheyProteinCreate, BrandCreate

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
# Brand CRUD operations
def create_brand(db: Session, brand: BrandCreate) -> BrandDB:
    db_brand = BrandDB(**brand.model_dump())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def get_brand(db: Session, brand_id: int) -> BrandDB:
    return db.query(BrandDB).filter(BrandDB.id == brand_id).first()

def get_brands(db: Session, skip: int = 0, limit: int = 100) -> List[BrandDB]:
    return db.query(BrandDB).offset(skip).limit(limit).all()

def get_brand_by_name(db: Session, name: str) -> BrandDB:
    return db.query(BrandDB).filter(BrandDB.name == name).first()

def update_brand(db: Session, brand_id: int, brand: BrandCreate) -> BrandDB:
    db_brand = db.query(BrandDB).filter(BrandDB.id == brand_id).first()
    if db_brand:
        for key, value in brand.model_dump().items():
            setattr(db_brand, key, value)
        db.commit()
        db.refresh(db_brand)
    return db_brand

def delete_brand(db: Session, brand_id: int) -> bool:
    db_brand = db.query(BrandDB).filter(BrandDB.id == brand_id).first()
    if db_brand:
        db.delete(db_brand)
        db.commit()
        return True
    return False