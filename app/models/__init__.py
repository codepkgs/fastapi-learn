from sqlalchemy.orm import declarative_base

from app.core.database import db_engine

Base = declarative_base()

if __name__ == "__main__":
    Base.metadata.create_all(bind=db_engine, checkfirst=True)
