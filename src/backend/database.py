from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL pointing to PostgreSQL service in Docker
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/detection_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)