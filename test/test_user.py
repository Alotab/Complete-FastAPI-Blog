
import requests 
from fastapi.testclient import TestClient 
# from sqlalchemy import create_engine

from app.schemas.user import UserCreate, UserOut
from app import main
from app.database.config import Base, get_db
from faker import Faker
from app.auth import oauth2
from app.routers import auth
import pytest
import pytest_asyncio


access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkB5YWhvby5jb20iLCJleHAiOjE2OTY5OTE5OTB9.zZ5YsLAQnodXBO6cA81RULtDkcoCtlNNG7T114H7DkI"



# SQLALCHEMY_DATABASE_URL = "sqlite://"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()

# client = TestClient(main.app)

    



from fastapi.testclient import TestClient
# from app import router
# from app.schemas import UserCreate

client = TestClient(main.app)

# Test the POST /users endpoint using the UserCreate schema
def test_create_user_with_schema():
    fake = Faker()
    user = UserCreate(
        username=fake.name(),
        email=fake.email(),
        password=fake.password()
    )

    response = client.post("/users", json=user.model_dump())
    assert response.status_code == 201
    assert isinstance(response.json(), dict)



def test_get_user_by_id_with_schema():
    fake = Faker()
    user_id = 1

    user_out = {"id": user_id, "email": fake.email()}
    response = client.get("/users/{}".format(user_id))
    assert response.status_code == 200

    user = response.json()
    assert isinstance(user, dict)

    # Validate the user schema
    user_schema = UserOut(**user_out)
    user_schema.model_validate(user)




@pytest.mark.asyncio
async def test_login_access_token():
    url = "http://127.0.0.1:8000/login/"

    user = {
        "email": "admin@yahoo.com",
        "password": "admin020"
    }

    response = await auth.login_for_access_token(get_db, form_data=user)
    assert response.status_code == 200
    # assert isinstance(response.json(), dict)
    print(response)
    # userAuth = oauth2.authenticat_user(get_db, userData['username'], userData['password'])
    # if userAuth:
    #     print("hi")

    # response = requests.get(url=url, data=userData)
    # assert "username" in response.json()

    # assert response.status_code == 200
