from sqlalchemy import String, Column, Date, Integer
from config.db import *
class TuongTac(Base):
    __tablename__ = "TuongTac"
    IDTT = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    IDUser = Column(String(100), nullable=False, default=None, unique=True)
    IDTD = Column(String(100), nullable=False, default=None, unique=True)
    ThoiDiem = Column(Date, nullable=False, default=None)
Base.metadata.create_all(bind=engine)