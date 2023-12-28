from config.db import SessionLocal
from pydantic import BaseModel, validator
from sqlalchemy import func, extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import Request, Depends, Form
from App.Model.TDEntity import *
from sqlalchemy import String, DateTime, UnicodeText    
from App.Model.PostModel import PostModel
from App.Model.TuongTacModel import *
class TDException(Exception):
    def __init__(self, message: str):
        self.message = message

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
def ConvertTD(td: TuyenDung):
    return {
        "IDTD": td.IDTD, 
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
        "LuongTD": td.LuongTD,
        "IDPost": td.IDPost
    }
class TDModel:
    def AddTD(self, td: TuyenDung):
        with SessionLocal() as db:
            try:
                db.add(td)
                db.commit()
                return True
            except IntegrityError as e:
                raise TDException("IDPost đã tồn tại hoặc không tồn tại")
            except Exception as e:
                raise TDException(getattr(e, 'message', repr(e)))
    def DeleteTD(self, IDTD: str):
        with SessionLocal() as db:
            try:
                postModel = PostModel()
                IDPost = self.GetTDByIDTD(IDTD).IDPost
                postModel.DeletePostByIDPost(IDPost)
                db.query(TuyenDung).filter(TuyenDung.IDTD == IDTD).delete()
                db.commit()
                return True
            except Exception:
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
                    "LuongTD": td.LuongTD,
                    "IDPost": td.IDPost
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
                listTDConvert.append(
                    ConvertTD(TD)
                )
            return listTDConvert
    def GetTDByIDTD(self, IDTD: str):
        with SessionLocal() as db:
            try:
                return db.query(TuyenDung).filter(TuyenDung.IDTD == IDTD).first()
            except Exception:
                raise TDException("Lấy tuyển dụng theo IDTD thất bại")
    def GetTDTuongTac(self):
        with SessionLocal() as db:
            try:
                interaction_count = func.count(TuongTac.IDTD)
                listTD = db.query(TuyenDung, interaction_count)\
                        .join(TuongTac, TuyenDung.IDTD == TuongTac.IDTD)\
                        .filter(
                            extract('month', TuyenDung.NgayTD) == extract('month', func.now()),
                            extract('year', TuyenDung.NgayTD) == extract('year', func.now())
                        )\
                        .group_by(TuyenDung.IDTD)\
                        .all()
                listTDConvert = []
                for TD, count in listTD:
                    listTDConvert.append(
                        {**ConvertTD(TD), **{"count": count}}
                    )
                return listTDConvert
            except Exception:
                raise TDException("Lấy tuyển dụng tương tác thất bại")
    def TimKiemTDByID(self, IDTD: str):
        with SessionLocal() as db:
            res = []
            try:
                res = db.query(TuyenDung).filter(TuyenDung.IDTD.like('%'+IDTD+'%')).all()
                if(res == None):
                    return None
                listTDConvert = []
                for TD in res:
                    listTDConvert.append(ConvertTD(TD))
                return listTDConvert
            except Exception as e:
                raise TDException("Tìm kiếm tuyển dụng theo ID thất bại, lỗi: ", e)
    def TimKiemTD(self, Text: str, LinhVucTD: str, DiaDiem: str):
        with SessionLocal() as db:
            res = []
            try:
                if(LinhVucTD == 'All' and DiaDiem == "All"):
                    res = db.query(TuyenDung).filter(
                        (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                        (TuyenDung.NoiTD.like('%'+Text+'%')) |
                        (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))
                    ).all()
                elif(LinhVucTD == "All" and DiaDiem != "All"):
                    res = db.query(TuyenDung).filter((
                        (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                        (TuyenDung.NoiTD.like('%'+Text+'%')) |
                        (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                        (TuyenDung.DiaDiem.like('%'+DiaDiem+'%'))
                    ).all()
                elif(LinhVucTD != "All" and DiaDiem == "All"):
                    res = db.query(TuyenDung).filter((
                        (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                        (TuyenDung.NoiTD.like('%'+Text+'%')) |
                        (TuyenDung.YeuCauCongViec.like('%'+Text+'%')))&
                        (TuyenDung.LinhVucTD == LinhVucTD)
                    ).all()
                else:
                    res = db.query(TuyenDung).filter((
                        (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                        (TuyenDung.NoiTD.like('%'+Text+'%')) |
                        (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                        (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                        (TuyenDung.LinhVucTD == LinhVucTD)
                    ).all()
                if(res == None):
                    return None
                listTDConvert = []
                for TD in res:
                    listTDConvert.append(ConvertTD(TD))
                return listTDConvert
            except Exception as e:
                raise TDException("Tìm kiếm tuyển dụng thất bại, lỗi: ", e)


