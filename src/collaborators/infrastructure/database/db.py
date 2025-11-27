from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.base import Base

# Configuration MySQL
DATABASE_URL = "mysql+pymysql://root:root@localhost/epic"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
