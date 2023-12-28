from sqlalchemy import Column, String, DateTime, UnicodeText, Double
from config.db import *
class TuyenDung(Base):
    __tablename__ = "TuyenDung"
    IDTD = Column(String, primary_key=True, nullable=False)
    NoiTD = Column(UnicodeText, nullable=True)
    NgayTD = Column(UnicodeText, nullable=True)
    SoLuongTD = Column(DateTime, nullable=True)
    LinhVucTD = Column(UnicodeText, nullable=True)
    ViTriTD = Column(UnicodeText, nullable=True)
    MotaCongViec = Column(UnicodeText, nullable=True)
    YeuCauCongViec = Column(UnicodeText, nullable=True)
    QuyenLoi = Column(UnicodeText, nullable=True)
    DiaDiem = Column(UnicodeText, nullable=True)
    SDT = Column(String, nullable=True)
    Gmail = Column(String, nullable=True)
    IDPost = Column(String, nullable=True)
    LuongTD = Column(Double, nullable=True)
Base.metadata.create_all(bind=engine)