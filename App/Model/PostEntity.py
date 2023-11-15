from sqlalchemy import Column, String, DateTime
from config.db import *
class Post(Base):
    __tablename__ = "Post"
    IDPost = Column(String, primary_key=True, notnull=True)
    TimePost = Column(DateTime, default=None)
    ContentPost = Column(String, notnull=True)
    IDUserSend = Column(String, notnull=True)
    NameUserSend = Column(String, notnull=True)
    LinkPost = Column(String, notnull=True)
    LinkImg = Column(String, notnull=True)
Base.metadata.create_all(bind=engine)
