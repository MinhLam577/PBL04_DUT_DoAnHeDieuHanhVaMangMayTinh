from App.Model.TuongTacEntity import TuongTac
from config.db import SessionLocal
from pydantic import BaseModel, validator
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import ssl
import smtplib
import numpy as np
import re
from datetime import datetime, timedelta, date
import datetime as dt
class TuongTacException(Exception):
    def __init__(self, message: str):
        self.message = message
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class TuongTacAdd(BaseModel):
    IDUser: str
    IDTD: str
    ThoiDiem: date = datetime.now().date()
class TuongTacDel(BaseModel):
    IDUser: str
    IDTD: str

class TuongTacModel:
    def GetAllTT(self):
        with SessionLocal() as db:
            listTT = db.query(TuongTac).all()
            listTTConvert = []
            for tt in listTT:
                IDTT = tt.IDTT
                IDUser = tt.IDUser
                IDTD = tt.IDTD
                ThoiDiem = tt.ThoiDiem
                listTTConvert.append({"IDTT": IDTT, "IDUser": IDUser, "IDTD": IDTD, "ThoiDiem": ThoiDiem})
            return listTTConvert
    def AddTT(self, tt: TuongTacAdd):
        with SessionLocal() as db:
            try:
                db.add(TuongTac(**tt.dict()))
                db.commit()
                return True
            except IntegrityError as e:
                raise TuongTacException("Bạn đã quan tâm bài tuyển dụng rồi")
            except Exception as e:
                raise TuongTacException(getattr(e, 'message', repr(e)))
    def DeleteTT(self, tt: TuongTacDel):
        with SessionLocal() as db:
            try:
                print(tt)
                db.query(TuongTac).filter((TuongTac.IDUser == tt.IDUser) & (TuongTac.IDTD == tt.IDTD)).delete()
                db.commit()
                return True
            except Exception:
                raise TuongTacException("Bạn chưa quan tâm bài tuyển dụng này")
    def DeleteTTByIDUser(self, IDUser: str):
        with SessionLocal() as db:
            try:
                db.query(TuongTac).filter(TuongTac.IDUser == IDUser).delete()
                db.commit()
                return True
            except Exception as e:
                raise TuongTacException(getattr(e, 'message', repr(e)))
    
    
