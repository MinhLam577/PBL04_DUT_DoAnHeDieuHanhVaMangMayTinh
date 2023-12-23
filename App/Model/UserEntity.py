from sqlalchemy import String, Column, Date
from config.db import *
class User(Base):
    __tablename__ = "User"
    IDUser = Column(String, primary_key=True, nullable=False)
    Gmail = Column(String, nullable=False, unique=True,default=None)
    Password = Column(String, nullable=False,default=None)
    QuyenUser = Column(String, nullable=False,default=None)
    ThoiGianDangKi = Column(Date, nullable=False, default=None)
Base.metadata.create_all(bind=engine)
