import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine
from infrastructure.persistence.schemas.schemas import Base
from infrastructure.config import settings

engine = create_engine(settings.database_url)
Base.metadata.create_all(engine)
print("✓ Migration complete")
