from sqlalchemy import Column, String, DateTime, UnicodeText
from config.db import *
class Post(Base):
    __tablename__ = "Post"
    IDPost = Column(String, primary_key=True, nullable=False)
    TimePost = Column(DateTime, default=None)
    ContentPost = Column(UnicodeText, nullable=False, unique=True)
    LinkPost = Column(String, nullable=False)
    LinkImg = Column(String)
Base.metadata.create_all(bind=engine)
