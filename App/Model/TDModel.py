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
                if td.SoLuongTD != None:
                    SoLuongTD = td.SoLuongTD 
                    if not re.match("^[0-9]+$", str(SoLuongTD)):
                        raise TDException("Số lượng tuyển dụng phải là số nguyên dương")
                    else:
                        if int(SoLuongTD) <= 0:
                            raise TDException("Số lượng tuyển dụng phải lớn hơn 0")
                if td.LuongTD != None:
                    LuongTD = td.LuongTD
                    if not re.match("^[0-9.]+$", str(LuongTD)):
                        raise TDException("Lương tuyển dụng phải là số dương")
                    else:
                        if(float(LuongTD) <= 0):
                            raise TDException("Lương tuyển dụng phải lớn hơn 0")
                if td.Gmail != None:
                    Gmail = td.Gmail
                    if not re.match("^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$", Gmail, re.IGNORECASE):
                        raise TDException('Gmail phải bao gồm ít nhất 5 ký tự, ít nhất 1 chữ cái và 1 số')
                if td.SDT != None:
                    SDT = td.SDT
                    if not re.match("^[0-9]+$", SDT, re.IGNORECASE) or not len(SDT) == 10:
                        raise TDException('Số điện thoại phải toàn số nguyên và có độ dài là 10')
                if td.NgayTD >= datetime.now():
                    raise TDException("Ngày tuyển dụng phải nhỏ hơn ngày hiện tại")
                db.add(td)
                db.commit()
                return True
            except ValueError:
                raise TDException("Lương tuyển dụng phải là số thực")
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
                if td.SoLuongTD != None:
                    SoLuongTD = td.SoLuongTD 
                    if not re.match("^[0-9]+$", str(SoLuongTD)):
                        raise TDException("Số lượng tuyển dụng phải là số nguyên dương")
                    else:
                        if int(SoLuongTD) <= 0:
                            raise TDException("Số lượng tuyển dụng phải lớn hơn 0")
                if td.LuongTD != None:
                    LuongTD = td.LuongTD
                    if not re.match("^[0-9.]+$", str(LuongTD)):
                        raise TDException("Lương tuyển dụng phải là số dương")
                    else:
                        if(float(LuongTD) <= 0):
                            raise TDException("Lương tuyển dụng phải lớn hơn 0")
                if td.Gmail != None:
                    Gmail = td.Gmail
                    if not re.match("^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$", Gmail, re.IGNORECASE):
                        raise TDException('Gmail phải bao gồm ít nhất 5 ký tự, ít nhất 1 chữ cái và 1 số')
                if td.SDT != None:
                    SDT = td.SDT
                    if not re.match("^[0-9]+$", SDT, re.IGNORECASE) or not len(SDT) == 10:
                        raise TDException('Số điện thoại phải toàn số nguyên và có độ dài là 10')
                if td.NgayTD >= datetime.now():
                    raise TDException("Ngày tuyển dụng phải nhỏ hơn ngày hiện tại")
                print("Đến đây")
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
            except Exception as e:
                raise TDException(getattr(e, 'message', repr(e)))
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
    def TimKiemTD(self, Text: str, LinhVucTD: str, DiaDiem: str, LuongTD: str):
        with SessionLocal() as db:
            res = []
            try:
                if(LinhVucTD == "All" and DiaDiem == "All" and LuongTD == "All"):
                    res = db.query(TuyenDung).filter(
                        (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                        (TuyenDung.NoiTD.like('%'+Text+'%')) |
                        (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))
                    ).all()
                elif(LinhVucTD == "All" and DiaDiem != "All" and LuongTD != "All"):
                    if(LuongTD == "None"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                            (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                            (TuyenDung.LuongTD == None)
                        ).all()
                    elif(LuongTD == "Below1M"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                            (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                            (TuyenDung.LuongTD < 10**6)
                        ).all()
                    elif(LuongTD == "Above50M"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                            (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                            (TuyenDung.LuongTD > 50*10**6)
                        ).all()
                    else:
                        start = int(LuongTD.split("-")[0]) * 10**6
                        end = int(LuongTD.split("-")[1]) * 10**6 - 1
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                            (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                            (TuyenDung.LuongTD.between(start, end))
                        ).all()
                elif(LinhVucTD != "All" and DiaDiem == "All" and LuongTD != "All"):
                    if(LuongTD == "None"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%')))&
                            (TuyenDung.LinhVucTD == LinhVucTD) &
                            (TuyenDung.LuongTD == None)
                        ).all()
                    elif(LuongTD == "Below1M"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%')))&
                            (TuyenDung.LinhVucTD == LinhVucTD) &
                            (TuyenDung.LuongTD < 10**6)
                        ).all()
                    elif(LuongTD == "Above50M"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%')))&
                            (TuyenDung.LinhVucTD == LinhVucTD) &
                            (TuyenDung.LuongTD > 50*10**6)
                        ).all()
                    else:
                        start = int(LuongTD.split("-")[0]) * 10**6
                        end = int(LuongTD.split("-")[1]) * 10**6 - 1
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%')))&
                            (TuyenDung.LinhVucTD == LinhVucTD) &
                            (TuyenDung.LuongTD.between(start, end))
                        ).all()
                elif(LinhVucTD != "All" and DiaDiem != "All" and LuongTD == "All"):
                    res = db.query(TuyenDung).filter((
                        (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                        (TuyenDung.NoiTD.like('%'+Text+'%')) |
                        (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                        (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                        (TuyenDung.LinhVucTD == LinhVucTD)
                    ).all()
                elif(LinhVucTD != "All" and DiaDiem == "All" and LuongTD == "All"):
                    res = db.query(TuyenDung).filter((
                        (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                        (TuyenDung.NoiTD.like('%'+Text+'%')) |
                        (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                        (TuyenDung.LinhVucTD == LinhVucTD)
                    ).all()
                elif(LinhVucTD == "All" and DiaDiem != "All" and LuongTD == "All"):
                    res = db.query(TuyenDung).filter((
                        (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                        (TuyenDung.NoiTD.like('%'+Text+'%')) |
                        (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                        (TuyenDung.DiaDiem.like('%'+DiaDiem+'%'))
                    ).all()
                elif(LinhVucTD == "All" and DiaDiem == "All" and LuongTD != "All"):
                    if(LuongTD == "None"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                            (TuyenDung.LuongTD == None)
                        ).all()
                    elif(LuongTD == "Below1M"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                            (TuyenDung.LuongTD < 10**6)
                        ).all()
                    elif(LuongTD == "Above50M"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                            (TuyenDung.LuongTD > 50*10**6)
                        ).all()
                    else:
                        start = int(LuongTD.split("-")[0]) * 10**6
                        end = int(LuongTD.split("-")[1]) * 10**6 - 1
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%'))) &
                            (TuyenDung.LuongTD.between(start, end))
                        ).all()
                elif(LinhVucTD != "All" and DiaDiem != "All" and LuongTD != "All"):
                    if(LuongTD == "None"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%')))&
                            (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                            (TuyenDung.LinhVucTD == LinhVucTD) &
                            (TuyenDung.LuongTD == None)
                        ).all()
                    elif(LuongTD == "Below1M"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%')))&
                            (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                            (TuyenDung.LinhVucTD == LinhVucTD) &
                            (TuyenDung.LuongTD < 10**6)
                        ).all()
                    elif(LuongTD == "Above50M"):
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%')))&
                            (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                            (TuyenDung.LinhVucTD == LinhVucTD) &
                            (TuyenDung.LuongTD > 50*10**6)
                        ).all()
                    else:
                        start = int(LuongTD.split("-")[0]) * 10**6
                        end = int(LuongTD.split("-")[1]) * 10**6 - 1
                        res = db.query(TuyenDung).filter((
                            (TuyenDung.ViTriTD.like('%'+Text+'%')) |
                            (TuyenDung.NoiTD.like('%'+Text+'%')) |
                            (TuyenDung.YeuCauCongViec.like('%'+Text+'%')))&
                            (TuyenDung.DiaDiem.like('%'+DiaDiem+'%')) &
                            (TuyenDung.LinhVucTD == LinhVucTD) &
                            (TuyenDung.LuongTD.between(start, end))
                        ).all()
                if(res == None):
                    return None
                listTDConvert = []
                for TD in res:
                    listTDConvert.append(ConvertTD(TD))
                return listTDConvert
            except Exception as e:
                raise TDException("Tìm kiếm tuyển dụng thất bại, lỗi: ", e)


