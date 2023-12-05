from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from auth import oauth2
from models import vote
# from models import user
from models import post as modelPost
from schemas import post as schemaPost
from database import config


router = APIRouter(prefix="/posts", tags=['Posts'])

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemaPost.PostOut]) 
async def get_posts(db: Session = Depends(config.get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    result_votes = db.query(modelPost.Post, func.count(vote.Vote.post_id).label("votes")).join(vote.Vote, vote.Vote.post_id == modelPost.Post.id, isouter=True).group_by(modelPost.Post.id).filter(modelPost.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()
    return result_votes



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemaPost.Post)
async def create_posts(post: schemaPost.PostCreate, db: Session = Depends(config.get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = modelPost.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemaPost.PostOut)
def get_post(id: int, db: Session = Depends(config.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(modelPost.Post, func.count(vote.Vote.post_id).label("votes")).join(vote.Vote, vote.Vote.post_id == modelPost.Post.id, isouter=True).group_by(modelPost.Post.id).filter(modelPost.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="item with id: {id} not found")
    return post



@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(config.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(modelPost.Post).filter(modelPost.Post.id == id)

    post = post_query.first()
    print(post.owner_id)

    if post.owner_id == None:
        raise HTTPException(status_code=404, detail="item not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform this request")
    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "posts was successfully deleted"}


@router.put("/{id}", response_model=schemaPost.Post)
def update_post(id: int, post: schemaPost.PostCreate, db: Session = Depends(config.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(modelPost.Post).filter(modelPost.Post.id == id)
    post_check = post_query.first()

    if  post_check == None:
        raise HTTPException(status_code=404, detail=f"item with id:{id} not found")
    
    if post_check.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform this request")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()