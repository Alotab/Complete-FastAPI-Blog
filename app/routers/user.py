from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from schemas import user as userSchema
from models import user as userModel
from utils import hash
from database import config


router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=userSchema.UserOut)
def  create_user(user: userSchema.UserCreate, db: Session = Depends(config.get_db)):

    hashed_password = hash(user.password)

    user.password = hashed_password
    new_user = userModel.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=userSchema.UserOut) 
def get_user(id: int, db: Session = Depends(config.get_db)):
    user = db.query(userModel.User).filter(userModel.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    
    return user