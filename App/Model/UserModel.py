from App.Model.UserEntity import User, Base
from config.db import SessionLocal, engine
from pydantic import BaseModel, validator
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import Request, Depends, Form
from email.message import EmailMessage
import ssl
import smtplib
import numpy as np
import re
class UvicornExeception(Exception):
    def __init__(self, message: str):
        self.message = message

Base.metadata.create_all(bind=engine)

def SendMail(message, receiveMail):
    Email_sender = "lambachu352@gmail.com"
    Email_Password = "bewh hhfx mxqd qqfy"
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = "Forgot Password"
    msg['From'] = Email_sender
    msg['To'] = receiveMail
    msg.set_content(message)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(Email_sender, Email_Password)
        server.sendmail(Email_sender, receiveMail, msg.as_string())
class UserLogin(BaseModel):
    Gmail: str 
    Password: str
    @validator('Gmail')
    def gmail_validator(cls, Gmail):
        if not re.match("^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$", Gmail, re.IGNORECASE):
            raise UvicornExeception('Định dạng email không hợp lệ')
        return Gmail
    @validator('Password')
    def password_validator(cls, Password):
        if not re.match("^(?=.*[a-z])(?=.*\d)[a-z\d]{5,}$", Password, re.IGNORECASE):
            raise UvicornExeception('Mật khẩu phải bao gồm ít nhất 5 ký tự, ít nhất 1 chữ cái và 1 số')
        return Password
    
class UserRegister(UserLogin):
    IDUser: str = "user" + str(np.random.randint(10000, 999999))
    QuyenUser: str = "user"
    NhapLai: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class UserModel:
    def GetAllUser(self):
        with SessionLocal() as db:
            rows = db.execute(text("SELECT * FROM User")).fetchall()
            listObject = []
            for row in rows:
                IDUser = row[0]
                Gmail = row[1]
                Password = row[2]
                QuyenUser = row[3]
                IDTD = row[4]
                listObject.append({'IDUser': IDUser, 'Gmail': Gmail, 'Password': Password, 'QuyenUser': QuyenUser, 'IDTD': IDTD})
            return listObject
    def CheckLogin(self, Gmail, Password):
        with SessionLocal() as db:
            us = db.execute(text("SELECT * FROM User WHERE Gmail = :Gmail"), {'Gmail': Gmail}).first()
            if(us == None):
                raise UvicornExeception('Gmail không tồn tại')
            else:
                if(us[2] != Password):
                    raise UvicornExeception('Mật khẩu không chính xác')
                else:
                    return us[3]
    def ForgotPassword(self, Gmail):
        with SessionLocal() as db:
            us = db.execute(text("SELECT * FROM User WHERE Gmail = :Gmail"), {'Gmail': Gmail}).first()
            if(us == None):
                raise UvicornExeception('Gmail không tồn tại')
            else:
                Password = us.Password
                message = "Mật khẩu của bạn là: " + Password
                SendMail(message, Gmail)
                return JSONResponse(
                    content={"message": "Mật khẩu đã được gửi đến Gmail của bạn"},
                )
    def AddUser(self, user):
        with SessionLocal() as db:
            IDUser = user.IDUser
            us = db.query(User).filter(User.IDUser == IDUser).first()
            if(us != None):
                while(us != None):
                    IDUser = "user" + str(np.random.randint(10000, 999999))
                    us = db.query(User).filter(User.IDUser == IDUser).first()
            Gmail = user.Gmail
            NhapLai = user.NhapLai
            Password = user.Password
            if(Password != NhapLai):
                raise UvicornExeception('Nhập lại mật khẩu không khớp')
            us = db.query(User).filter(User.Gmail == Gmail).first()
            if(us != None):
                raise UvicornExeception('Gmail đã tồn tại')
            db.add(User(IDUser = IDUser, Gmail = Gmail, Password = Password, QuyenUser = user.QuyenUser))
            db.commit()
            return user



