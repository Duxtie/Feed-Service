from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from app.db.base import Base
from app.api.deps import get_db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import SessionLocal
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


app.dependency_overrides[get_db] = db