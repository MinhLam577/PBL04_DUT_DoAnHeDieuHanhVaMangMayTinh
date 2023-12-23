from config.db import SessionLocal
from pydantic import BaseModel, validator
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import Request, Depends, Form
from App.Model.TDEntity import *
from sqlalchemy import String, DateTime, UnicodeText    
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
                return True
            except Exception:
                raise TDException("Thêm tuyển dụng thất bại")
    def DeleteTD(self, IDTD: str):
        with SessionLocal() as db:
            try:
                db.query(TuyenDung).filter(TuyenDung.IDTD == IDTD).delete()
                db.commit()
                return True
            except Exception:
                print("Xóa thất bại")
                raise TDException("Xóa tuyển dụng thất bại")
    def UpdateTD(self, td: TuyenDung):
        with SessionLocal() as db:
            try:
                db.query(TuyenDung).filter(TuyenDung.IDTD == td.IDTD).update({
                    "NoiTD": td.NoiTD, 
                    "NgayTD": td.NgayTD, 
                    "SoLuongTD": td.SoLuongTD, 
                    "LinhVucTD": td.LinhVucTD, 
                    "ViTriTD": td.ViTriTD, 
                    "MotaCongViec": td.MotaCongViec, 
                    "YeuCauCongViec": td.YeuCauCongViec, 
                    "QuyenLoi": td.QuyenLoi, 
                    "DiaDiem": td.DiaDiem, 
                    "SDT": td.SDT, 
                    "Gmail": td.Gmail, 
                    "LuongTD": td.LuongTD
                })
                db.commit()
                return True
            except Exception:
                raise TDException("Cập nhật tuyển dụng thất bại")
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
                MotaCongViec = TD.MotaCongViec
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
                    "MotaCongViec": MotaCongViec, 
                    "YeuCauCongViec": YeuCauCongViec, 
                    "QuyenLoi": QuyenLoi, 
                    "DiaDiem": DiaDiem, 
                    "SDT": SDT, 
                    "Gmail": Gmail, 
                    "LuongTD": LuongTD
                })
            return listTDConvert
    def GetTDByIDTD(self, IDTD: str):
        with SessionLocal() as db:
            try:
                return db.query(TuyenDung).filter(TuyenDung.IDTD == IDTD).first()
            except Exception:
                raise TDException("Lấy tuyển dụng theo IDTD thất bại")
    def DeleteOldTD(self):  
        with SessionLocal() as db:
            try:
                db.execute(text("CALL DeleteOldTD"))
                db.commit()
                return True
            except Exception:
                raise TDException("Xóa tuyển dụng cũ thất bại")
    def TimKiemTD(self, Text: str, LinhVucTD: str, DiaDiem: str):
        with SessionLocal() as db:
            res = None
            try:
                if(LinhVucTD == 'All' and DiaDiem == "All"):
                    res = db.execute(text(f"CALL SearchTuyenDung('{Text}', '{Text}', '{Text}', '', '')")).fetchall()
                elif(LinhVucTD == "All" and DiaDiem != "All"):
                    res = db.execute(text(f"CALL SearchTuyenDung('{Text}', '{Text}', '{Text}', '', '{DiaDiem}')")).fetchall()
                elif(LinhVucTD != "All" and DiaDiem == "All"):
                    res = db.execute(text(f"CALL SearchTuyenDung('{Text}', '{Text}', '{Text}', '{LinhVucTD}', '')")).fetchall()
                if(res != None):
                    return res
            except Exception as e:
                raise TDException("Tìm kiếm tuyển dụng thất bại, lỗi: ", e)