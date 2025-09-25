from contextlib import contextmanager

from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

db_engine = create_engine(
    f"mysql+pymysql://{settings.database.user}:{settings.database.password}@{settings.database.host}:{settings.database.port}/{settings.database.dbname}?charset={settings.database.charset}",
    poolclass=QueuePool,
    max_overflow=settings.database.max_overflow,
    pool_size=settings.database.pool_size,
    pool_timeout=settings.database.pool_timeout,
    pool_recycle=settings.database.pool_recycle,
    pool_pre_ping=settings.database.pool_pre_ping,
    echo=settings.database.echo,
)

session_factory = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)
SessionLocal = scoped_session(session_factory)


@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        SessionLocal.remove()
