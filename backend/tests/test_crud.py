import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, WheyProteinDB
from src.api.crud import create_whey_protein, get_whey_protein, get_whey_proteins, update_whey_protein, delete_whey_protein
from src.api.schemas import WheyProteinCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_crud.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_whey_protein(db_session):
    whey_data = WheyProteinCreate(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25,
        leucina=2500  # This will be converted from mg to g (2.5)
    )
    
    created_whey = create_whey_protein(db_session, whey_data)
    
    assert created_whey.id is not None
    assert created_whey.name == "Test Whey"
    assert created_whey.price == 100.0
    assert created_whey.leucina == 2.5  # Converted from 2500mg to 2.5g

def test_get_whey_protein(db_session):
    whey_data = WheyProteinCreate(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25
    )
    
    created_whey = create_whey_protein(db_session, whey_data)
    retrieved_whey = get_whey_protein(db_session, created_whey.id)
    
    assert retrieved_whey is not None
    assert retrieved_whey.id == created_whey.id
    assert retrieved_whey.name == "Test Whey"

def test_get_whey_proteins(db_session):
    whey_data1 = WheyProteinCreate(
        name="Test Whey 1",
        price=100.0,
        brand="Brand 1",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25
    )
    
    whey_data2 = WheyProteinCreate(
        name="Test Whey 2",
        price=150.0,
        brand="Brand 2",
        serving_size=35,
        total_weight=1000,
        protein_per_serving=30
    )
    
    create_whey_protein(db_session, whey_data1)
    create_whey_protein(db_session, whey_data2)
    
    whey_proteins = get_whey_proteins(db_session)
    
    assert len(whey_proteins) == 2
    assert whey_proteins[0].name == "Test Whey 1"
    assert whey_proteins[1].name == "Test Whey 2"

def test_update_whey_protein(db_session):
    whey_data = WheyProteinCreate(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25
    )
    
    created_whey = create_whey_protein(db_session, whey_data)
    
    updated_data = WheyProteinCreate(
        name="Updated Whey",
        price=120.0,
        brand="Updated Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25,
        leucina=3000  # This will be converted from mg to g (3.0)
    )
    
    updated_whey = update_whey_protein(db_session, created_whey.id, updated_data)
    
    assert updated_whey.name == "Updated Whey"
    assert updated_whey.price == 120.0
    assert updated_whey.brand == "Updated Brand"
    assert updated_whey.leucina == 3.0  # Converted from 3000mg to 3.0g

def test_delete_whey_protein(db_session):
    whey_data = WheyProteinCreate(
        name="Test Whey",
        price=100.0,
        brand="Test Brand",
        serving_size=30,
        total_weight=900,
        protein_per_serving=25
    )
    
    created_whey = create_whey_protein(db_session, whey_data)
    
    success = delete_whey_protein(db_session, created_whey.id)
    assert success is True
    
    deleted_whey = get_whey_protein(db_session, created_whey.id)
    assert deleted_whey is None

def test_delete_nonexistent_whey_protein(db_session):
    success = delete_whey_protein(db_session, 999)
    assert success is False