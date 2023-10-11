from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

# from database.config import Base
from ..database.config import Base

if TYPE_CHECKING:
    from .post import Post

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    #testing
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    posts = relationship("Post", back_populates="owner")