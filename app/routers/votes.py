from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from ..schemas import votes
from ..models import post as modelPost
from ..models import vote as modelVote
from ..database import config
from ..auth import oauth2

router = APIRouter(prefix='/vote', tags=['VOTE'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: votes.Vote, db: Session = Depends(config.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(modelPost.Post).filter(modelPost.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{vote.post_id} does not exist")

    vote_query =  db.query(modelVote.Vote).filter(modelVote.Vote.post_id == vote.post_id, modelVote.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already votes on post {vote.post_id}")

        new_vote = modelVote.Vote(post_id= vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
       
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}

