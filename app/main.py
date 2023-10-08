from fastapi import FastAPI
# from . import models

from routers import auth, user, post, votes
from database.config import engine, Base


Base.metadata.create_all(bind=engine)



app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def test():
    return {"message": "hello world"}