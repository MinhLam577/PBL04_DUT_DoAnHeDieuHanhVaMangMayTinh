from sqlalchemy import String, Column
from config.db import *
class User(Base):
    __tablename__ = "User"
    IDUser = Column(String, primary_key=True, nullable=False)
    Gmail = Column(String, nullable=False, unique=True)
    Password = Column(String, nullable=False)
    QuyenUser = Column(String, nullable=False)
    IDTD = Column(String, nullable=True, default=None)

