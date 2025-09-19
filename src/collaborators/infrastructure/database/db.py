from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.base import Base

DATABASE_URL = "sqlite:///epic.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_session():
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()


def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
