# -------------------------------- sqlalchemy imports ---------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# -------------------------------- settings imports ---------------------------
from constants.config import env_variables

engine = create_engine(
    env_variables.DATABASE_URL, echo=False, pool_pre_ping=True, pool_recycle=280,
    isolation_level="READ UNCOMMITTED", pool_size=500, max_overflow=100
)


def get_db_session():
    """
    This function yields a db_session and closes at the end of api call
    :return: None
    """
    SessionLocal = sessionmaker(
        bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
    db = SessionLocal()
    """:type: sqlalchemy.orm.Session"""
    try:
        yield db
    finally:
        db.close()


def get_db_session_to_variable() -> Session:
    """
    This function will return a db_session
    that session should be closed manually
    :param schema:
    :return:
    """
    SessionLocal = sessionmaker(
        bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
    db = SessionLocal()
    """:type: sqlalchemy.orm.Session"""
    return db
