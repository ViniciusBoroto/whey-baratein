from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.domain.models.brand import Brand
from ..database.database import get_db
from ..database.models import WheyProteinDB, BrandDB
from ..domain.models.whey_protein import WheyProtein
from ..api import crud, schemas

router = APIRouter(prefix="/whey-proteins", tags=["whey-proteins"])

def db_to_domain(db_whey_protein: WheyProteinDB) -> WheyProtein:
    data = {k: v for k, v in db_whey_protein.__dict__.items() if not k.startswith('_')}
    # Handle None values for new fields
    if data.get('reliability') is None:
        data['reliability'] = 0
    if data.get('image_url') is None:
        data['image_url'] = None
    # Convert brand relationship to string for domain model
    if db_whey_protein.brand_rel:
        data['brand'] = Brand(**db_whey_protein.brand_rel.__dict__)
    else:
        data['brand'] = 'Unknown'
    # Remove brand_id and brand_rel from data
    data.pop('brand_id', None)
    data.pop('brand_rel', None)
    return WheyProtein(**data)

@router.post("/", response_model=schemas.WheyProteinResponse)
def create_whey_protein(whey_protein: schemas.WheyProteinCreate, db: Session = Depends(get_db)):
    db_whey_protein = crud.create_whey_protein(db=db, whey_protein=whey_protein)
    domain_whey_protein = db_to_domain(db_whey_protein)
    
    # Create response with brand info
    response_data = db_whey_protein.__dict__.copy()
    response_data['brand'] = db_whey_protein.brand_rel.__dict__ if db_whey_protein.brand_rel else None
    response_data['eea_per_serving'] = domain_whey_protein.eea_per_serving()
    response_data['servings_per_packet'] = domain_whey_protein.servings_per_packet()
    response_data['total_eea_per_packet'] = domain_whey_protein.total_eea_per_packet()
    response_data['eea_price'] = domain_whey_protein.eea_price()
    response_data['protein_concentration'] = domain_whey_protein.protein_concentration()
    
    return response_data

@router.get("/{whey_protein_id}", response_model=schemas.WheyProteinResponse)
def read_whey_protein(whey_protein_id: int, db: Session = Depends(get_db)):
    db_whey_protein = crud.get_whey_protein(db, whey_protein_id=whey_protein_id)
    if db_whey_protein is None:
        raise HTTPException(status_code=404, detail="Whey protein not found")
    
    domain_whey_protein = db_to_domain(db_whey_protein)
    return schemas.WheyProteinResponse(
        **db_whey_protein.__dict__,
        eea_per_serving=domain_whey_protein.eea_per_serving(),
        servings_per_packet=domain_whey_protein.servings_per_packet(),
        total_eea_per_packet=domain_whey_protein.total_eea_per_packet(),
        eea_price=domain_whey_protein.eea_price(),
        protein_concentration=domain_whey_protein.protein_concentration()
    )

@router.get("/", response_model=List[schemas.WheyProteinResponse])
def read_whey_proteins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    whey_proteins = crud.get_whey_proteins(db, skip=skip, limit=limit)
    result = []
    for wp in whey_proteins:
        domain_wp = db_to_domain(wp)
        result.append(schemas.WheyProteinResponse(
            **domain_wp.__dict__,
            eea_per_serving=domain_wp.eea_per_serving(),
            servings_per_packet=domain_wp.servings_per_packet(),
            total_eea_per_packet=domain_wp.total_eea_per_packet(),
            eea_price=domain_wp.eea_price(),
            protein_concentration=domain_wp.protein_concentration()
        ))
    return result

@router.put("/{whey_protein_id}", response_model=schemas.WheyProteinResponse)
def update_whey_protein(whey_protein_id: int, whey_protein: schemas.WheyProteinCreate, db: Session = Depends(get_db)):
    db_whey_protein = crud.update_whey_protein(db, whey_protein_id=whey_protein_id, whey_protein=whey_protein)
    if db_whey_protein is None:
        raise HTTPException(status_code=404, detail="Whey protein not found")
    
    domain_whey_protein = db_to_domain(db_whey_protein)
    return schemas.WheyProteinResponse(
        **db_whey_protein.__dict__,
        eea_per_serving=domain_whey_protein.eea_per_serving(),
        servings_per_packet=domain_whey_protein.servings_per_packet(),
        total_eea_per_packet=domain_whey_protein.total_eea_per_packet(),
        eea_price=domain_whey_protein.eea_price(),
        protein_concentration=domain_whey_protein.protein_concentration()
    )

@router.delete("/{whey_protein_id}")
def delete_whey_protein(whey_protein_id: int, db: Session = Depends(get_db)):
    success = crud.delete_whey_protein(db, whey_protein_id=whey_protein_id)
    if not success:
        raise HTTPException(status_code=404, detail="Whey protein not found")
    return {"message": "Whey protein deleted successfully"}

@router.get("/rankings/eea-price", response_model=List[schemas.WheyProteinRanking])
def get_eea_price_ranking(db: Session = Depends(get_db)):
    whey_proteins = crud.get_whey_proteins(db)
    rankings = []
    
    for wp in whey_proteins:
        domain_wp = db_to_domain(wp)
        rankings.append({
            "id": wp.id,
            "name": wp.name,
            "brand": wp.brand_rel.name if wp.brand_rel else "Sem marca",
            "eea_price": domain_wp.eea_price(),
            "protein_concentration": domain_wp.protein_concentration()
        })
    
    rankings.sort(key=lambda x: x["eea_price"])
    
    for i, ranking in enumerate(rankings):
        ranking["rank"] = i + 1
    
    return rankings

@router.get("/rankings/protein-concentration", response_model=List[schemas.WheyProteinRanking])
def get_protein_concentration_ranking(db: Session = Depends(get_db)):
    whey_proteins = crud.get_whey_proteins(db)
    rankings = []
    
    for wp in whey_proteins:
        domain_wp = db_to_domain(wp)
        rankings.append({
            "id": wp.id,
            "name": wp.name,
            "brand": wp.brand_rel.name if wp.brand_rel else "Sem marca",
            "eea_price": domain_wp.eea_price(),
            "protein_concentration": domain_wp.protein_concentration()
        })
    
    rankings.sort(key=lambda x: x["protein_concentration"], reverse=True)
    
    for i, ranking in enumerate(rankings):
        ranking["rank"] = i + 1
    
    return rankings
# Brand routes
brand_router = APIRouter(prefix="/brands", tags=["brands"])

@brand_router.post("/", response_model=schemas.BrandResponse)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    # Check if brand already exists
    existing_brand = crud.get_brand_by_name(db, brand.name)
    if existing_brand:
        raise HTTPException(status_code=400, detail="Brand already exists")
    return crud.create_brand(db=db, brand=brand)

@brand_router.get("/{brand_id}", response_model=schemas.BrandResponse)
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id=brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brand

@brand_router.get("/", response_model=List[schemas.BrandResponse])
def read_brands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    brands = crud.get_brands(db, skip=skip, limit=limit)
    return brands

@brand_router.put("/{brand_id}", response_model=schemas.BrandResponse)
def update_brand(brand_id: int, brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    db_brand = crud.update_brand(db, brand_id=brand_id, brand=brand)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brand

@brand_router.delete("/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    success = crud.delete_brand(db, brand_id=brand_id)
    if not success:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"message": "Brand deleted successfully"}