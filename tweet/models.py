from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import BaseModel


class Tweet(BaseModel):
    text = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="tweets")
