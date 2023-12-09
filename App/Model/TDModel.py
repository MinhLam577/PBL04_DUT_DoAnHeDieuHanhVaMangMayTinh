from config.db import SessionLocal
from pydantic import BaseModel, validator
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import Request, Depends, Form
from App.Model.TDEntity import *

class TDException(Exception):
    def __init__(self, message: str):
        self.message = message
        
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class TDModel:
    def AddTD(self, td: TuyenDung):
        with SessionLocal() as db:
            try:
                db.add(td)
                db.commit()
                db.refresh(td)
                return td
            except Exception:
                raise TDException("Thêm tuyển dụng thất bại")
    def GetAllTD(self):
        with SessionLocal() as db:
            listTD = db.query(TuyenDung).all()
            listTDConvert = []
            for TD in listTD:
                IDTD = TD.IDTD
                NoiTD = TD.NoiTD
                NgayTD = TD.NgayTD
                SoLuongTD = TD.SoLuongTD
                LinhVucTD = TD.LinhVucTD
                ViTriTD = TD.ViTriTD
                MoTaCongViec = TD.MoTaCongViec
                YeuCauCongViec = TD.YeuCauCongViec
                QuyenLoi = TD.QuyenLoi
                DiaDiem = TD.DiaDiem
                SDT = TD.SDT
                Gmail = TD.Gmail
                LuongTD = TD.LuongTD
                listTDConvert.append({
                    "IDTD": IDTD, 
                    "NoiTD": NoiTD, 
                    "NgayTD": NgayTD, 
                    "SoLuongTD": SoLuongTD, 
                    "LinhVucTD": LinhVucTD, 
                    "ViTriTD": ViTriTD, 
                    "MoTaCongViec": MoTaCongViec, 
                    "YeuCauCongViec": YeuCauCongViec, 
                    "QuyenLoi": QuyenLoi, 
                    "DiaDiem": DiaDiem, 
                    "SDT": SDT, 
                    "Gmail": Gmail, 
                    "LuongTD": LuongTD
                })
            return listTDConvert