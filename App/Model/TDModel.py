from config.db import SessionLocal
from pydantic import BaseModel, validator
from sqlalchemy import func, extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import Request, Depends, Form, UploadFile
from App.Model.TDEntity import *
from sqlalchemy import String, DateTime, UnicodeText    
from App.Model.PostModel import PostModel
from App.Model.TuongTacEntity import *
from App.Model.UserModel import *
import os
import io
import re
from datetime import datetime
import datetime as dt
from PIL import Image
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

async def Save_image(image, IDPost):
    try:
        image = Image.open(io.BytesIO(image))
        img = image.convert('RGB')
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(path + "/View/static/images/TDImages/" + IDPost + ".jpg", "wb") as f:
            img.save(f, "JPEG")
    except Exception as e:
        raise TDException(getattr(e, 'message', repr(e)))

def Delete_image(IDPost):
    try:
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/View/static/images/TDImages/" + IDPost + ".jpg"
        if os.path.exists(path) == False:
            return
        os.remove(path)
    except Exception as e:
        raise TDException(getattr(e, 'message', repr(e)))

class TDModel:
    async def AddTD(self, td: TuyenDung, image: UploadFile):
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
                if td.SDT != None:
                    SDT = td.SDT
                    if not re.match("^[0-9]+$", SDT, re.IGNORECASE) or not len(SDT) == 10:
                        raise TDException('Số điện thoại phải toàn số nguyên >= 0 và có độ dài là 10')
                if td.NgayTD >= datetime.now():
                    raise TDException("Ngày tuyển dụng phải nhỏ hơn ngày hiện tại")
                db.add(td)
                db.commit()
                filename = ""
                if(image.filename == None):
                    filename = ""
                else:   
                    filename = image.filename
                if(filename != ""):
                    await Save_image(await image.read(), td.IDPost)
                return True
            except ValueError:
                raise TDException("Lương tuyển dụng phải là số thực")
            except IntegrityError as e:
                raise TDException("IDPost đã tồn tại hoặc không tồn tại, chi tiết: " + getattr(e, 'message', repr(e)))
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
                Delete_image(IDPost)
                return True
            except Exception as e:
                raise TDException(getattr(e, 'message', repr(e)))
    async def UpdateTD(self, td: TuyenDung, image: UploadFile):
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
                if td.SDT != None:
                    SDT = td.SDT
                    if not re.match("^[0-9]+$", SDT, re.IGNORECASE) or not len(SDT) == 10:
                        raise TDException('Số điện thoại phải toàn số nguyên >= 0 và có độ dài là 10')
                if td.NgayTD >= datetime.now():
                    raise TDException("Ngày tuyển dụng phải nhỏ hơn ngày hiện tại")
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
                filename = ""
                if(image.filename == None):
                    filename = ""
                else:   
                    filename = image.filename
                if(filename != ""):
                    await Save_image(await image.read(), td.IDPost)
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
            except Exception as e:
                raise TDException(getattr(e, 'message', repr(e)))
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
                raise TDException(getattr(e, 'message', repr(e)))
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
                raise TDException(getattr(e, 'message', repr(e)))
    def GetListUserTuongTacByIDTD(self, IDTD: str):
        with SessionLocal() as db:
            try:
                res = db.query(User.IDUser, User.Gmail, TuongTac.ThoiDiem)\
                    .join(TuongTac, User.IDUser == TuongTac.IDUser)\
                    .filter(TuongTac.IDTD == IDTD).all()
                for i in range(len(res)):
                        res[i] = {"IDUser": res[i][0], "Gmail": res[i][1], "ThoiDiem": res[i][2]}
                return res    
            except Exception as e:
                raise TDException(getattr(e, 'message', repr(e)))
    def SearchUserByGmailAndIDTD(self, Gmail: str, IDTD: str):
        with SessionLocal() as db:
            try:
                res = db.query(User.IDUser, User.Gmail, TuongTac.ThoiDiem)\
                    .join(TuongTac, User.IDUser == TuongTac.IDUser)\
                    .filter(TuongTac.IDTD == IDTD, User.Gmail.like('%'+Gmail+'%')).all()
                for i in range(len(res)):
                        res[i] = {"IDUser": res[i][0], "Gmail": res[i][1], "ThoiDiem": res[i][2]}
                return res    
            except Exception as e:
                raise TDException(getattr(e, 'message', repr(e)))
    def SendGmail(self, IDTD: str):
        with SessionLocal() as db:
            try:
                listuser = self.GetListUserTuongTacByIDTD(IDTD)
                td = self.GetTDByIDTD(IDTD)
                if(len(listuser) > 0):
                    listGmail = [user["Gmail"] for user in listuser]
                    message = f""" 
Bài viết có ID là {IDTD} đã được thay đổi \n
Nội dung thay đổi là: \n
Nơi tuyển dụng: {td.NoiTD} \n
Ngày tuyển dụng: {td.NgayTD} \n
Số lượng tuyển dụng: {td.SoLuongTD} \n
Lĩnh vực tuyển dụng: {td.LinhVucTD} \n
Vị trí tuyển dụng: \n {td.ViTriTD} \n
Mô tả công việc: \n {td.MotaCongViec} \n
Yêu cầu công việc: \n {td.YeuCauCongViec} \n
Quyền lợi: \n {td.QuyenLoi} \n
Địa điểm: \n {td.DiaDiem} \n
Số điện thoại: {td.SDT} \n
Gmail: {td.Gmail} \n
Lương: {td.LuongTD} \n
"""
                    for gmail in listGmail:
                        SendMail(message, gmail, "Thông báo thay đổi bài tuyển dụng")
            except Exception as e:
                raise TDException(getattr(e, 'message', repr(e)))


