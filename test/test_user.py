

from fastapi.testclient import TestClient 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.schemas import user
from app import main
from app.database.config import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

client = TestClient(main.app)


def test_create_user():
    newUser = user.UserCreate(
        email="booosjhdsdssdsdsdusdsdsdshdgsy@ymail.com",
        password="1234567982jusssdssd",
    )
    response = client.post('/users/', json=newUser.model_dump())


    assert response.status_code == 201
    assert response.json() == user.UserOut(
        id=24,
        email="booosjhdsdssdsdsdusdsdsdshdgsy@ymail.com",
        created_at="2023-10-10T17:53:28.181331")