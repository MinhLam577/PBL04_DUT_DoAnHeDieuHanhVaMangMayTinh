from App.Model.UserEntity import User
from config.db import SessionLocal
from pydantic import BaseModel, validator
from sqlalchemy import text, extract, func
from fastapi.responses import JSONResponse
from email.message import EmailMessage
from sqlalchemy.exc import IntegrityError
import ssl
import smtplib
import numpy as np
import re
from datetime import datetime, timedelta, date
import datetime as dt

class UserExeception(Exception):
    def __init__(self, message: str):
        self.message = message
    
def SendMail(message, receiveMail, subject, subtype = "text/plain"):
    Email_sender = "lambachu352@gmail.com"
    Email_Password = "bewh hhfx mxqd qqfy"
    msg = EmailMessage()
    msg.set_content(message, subtype=subtype)
    msg['Subject'] = subject
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
    
class UserRegister(UserLogin):
    @validator('Gmail')
    def gmail_validator(cls, Gmail):
        if not re.match("^[a-z0-9](\.?[a-z0-9]){5,}@((g(oogle)?mail)|(dut\.udn))\.(com|vn)$", Gmail, re.IGNORECASE):
            raise UserExeception('Gmail phải bao gồm ít nhất 5 ký tự, đuôi có thể là @gmail.com, @dut.udn.vn, @googlemail.com')
        return Gmail
    @validator('Password')
    def password_validator(cls, Password):
        if not re.match("^(?=.*[a-z])(?=.*\d)[a-z\d]{5,}$", Password, re.IGNORECASE):
            raise UserExeception('Mật khẩu phải bao gồm ít nhất 5 ký tự, ít nhất 1 chữ cái và 1 số')
        return Password
    IDUser: str = "user" + str(np.random.randint(1, 999999))
    QuyenUser: str = "user"
    NhapLai: str

class UserUpdate(BaseModel):
    IDUser: str
    Gmail: str
    @validator('Gmail')
    def gmail_validator(cls, Gmail):
        if not re.match("^[a-z0-9](\.?[a-z0-9]){5,}@((g(oogle)?mail)|(dut\.udn))\.(com|vn)$", Gmail, re.IGNORECASE):
            raise UserExeception('Gmail phải bao gồm ít nhất 5 ký tự, đuôi có thể là @gmail.com, @dut.udn.vn, @googlemail.com')
        return Gmail
    Password: str
    @validator('Password')
    def password_validator(cls, Password):
        if not re.match("^(?=.*[a-z])(?=.*\d)[a-z\d]{5,}$", Password, re.IGNORECASE):
            raise UserExeception('Mật khẩu phải bao gồm ít nhất 5 ký tự, ít nhất 1 chữ cái và 1 số')
        return Password
    
class UserAdd(BaseModel):
    Gmail: str
    @validator('Gmail')
    def gmail_validator(cls, Gmail):
        if not re.match("^[a-z0-9](\.?[a-z0-9]){5,}@((g(oogle)?mail)|(dut\.udn))\.(com|vn)$", Gmail, re.IGNORECASE):
            raise UserExeception('Gmail phải bao gồm ít nhất 5 ký tự, đuôi có thể là @gmail.com, @dut.udn.vn, @googlemail.com')
        return Gmail
    Password: str
    @validator('Password')
    def password_validator(cls, Password):
        if not re.match("^(?=.*[a-z])(?=.*\d)[a-z\d]{5,}$", Password, re.IGNORECASE):
            raise UserExeception('Mật khẩu phải bao gồm ít nhất 5 ký tự, ít nhất 1 chữ cái và 1 số')
        return Password
    IDUser: str = "user" + str(np.random.randint(1, 999999))
    QuyenUser: str = "user"
    ThoiGianDangKi: date = datetime.now().date()
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
                listObject.append({'IDUser': IDUser, 'Gmail': Gmail, 'Password': Password, 'QuyenUser': QuyenUser})
            return listObject
    def GetUserByGmail(self, Gmail: str):
        with SessionLocal() as db:
            return db.query(User).filter(User.Gmail == Gmail).first()
    def CheckLogin(self, Gmail, Password):
        with SessionLocal() as db:
            us = db.execute(text("SELECT * FROM User WHERE Gmail = :Gmail"), {'Gmail': Gmail}).first()
            if(us == None):
                raise UserExeception('Gmail không tồn tại')
            else:
                if(us[2] != Password):
                    raise UserExeception('Mật khẩu không chính xác')
                else:
                    return us[3]
    def ForgotPassword(self, Gmail):
        with SessionLocal() as db:
            us = db.execute(text("SELECT * FROM User WHERE Gmail = :Gmail"), {'Gmail': Gmail}).first()
            if(us == None):
                raise UserExeception('Gmail không tồn tại')
            else:
                Password = us.Password
                message = "Mật khẩu của bạn là: " + Password
                SendMail(message, Gmail, "Forgot Password", "text/plain")
                return JSONResponse(
                    content={"message": "Mật khẩu đã được gửi đến Gmail của bạn"},
                )
    def UpdateUser(self, user: UserUpdate):
        with SessionLocal() as db:
            try:
                us = db.query(User).filter(User.IDUser == user.IDUser).first()
                if(us == None):
                    raise UserExeception("IDUser không tồn tại")
                else:
                    us = db.query(User).filter(User.IDUser == user.IDUser).update({
                        "Gmail": user.Gmail,
                        "Password": user.Password
                    })
                    db.commit()
                    return True
            except IntegrityError:
                raise UserExeception('Gmail đã tồn tại')
            except Exception as e:
                raise UserExeception(getattr(e, 'message', repr(e)))
    def DeleteUserByGmail(self, Gmail: str):
        with SessionLocal() as db:
            try:
                us = db.query(User).filter(User.Gmail == Gmail).first()
                if(us == None):
                    raise UserExeception("Gmail không tồn tại")
                else:
                    db.query(User).filter(User.Gmail == Gmail).delete()
                    db.commit()
                    return True
            except UserExeception:
                raise UserExeception('Gmail không tồn tại')
            except Exception as e:
                raise UserExeception(getattr(e, 'message', repr(e)))
    def AddUser(self, user: UserAdd):
        with SessionLocal() as db:
            try:
                us = db.query(User).filter(User.Gmail == user.Gmail).first()
                if(us != None):
                    raise UserExeception("Gmail đã tồn tại")
                else:
                    listUserID = [record[0] for record in db.query(User.IDUser).all()]
                    IDUser = user.IDUser
                    while IDUser in listUserID:
                        IDUser = "user" + str(np.random.randint(1, 999999))
                    db.add(User(IDUser = user.IDUser, Gmail = user.Gmail, Password = user.Password, 
                                QuyenUser = user.QuyenUser, ThoiGianDangKi = user.ThoiGianDangKi))
                    db.commit()
                    return True
            except UserExeception:
                raise UserExeception('Gmail đã tồn tại')
            except Exception as e:
                raise UserExeception(getattr(e, 'message', repr(e)))
    def AddUserRegister(self, user):
        with SessionLocal() as db:
            listUserID = [record[0] for record in db.query(User.IDUser).all()]
            IDUser = user.IDUser
            while IDUser in listUserID:
                IDUser = "user" + str(np.random.randint(1, 999999))
            Gmail = user.Gmail
            NhapLai = user.NhapLai
            Password = user.Password
            ThoiGianDangKi = date.today().strftime("%Y-%m-%d")
            if(Password != NhapLai):
                raise UserExeception('Nhập lại mật khẩu không khớp')
            us = db.query(User).filter(User.Gmail == Gmail).first()
            if(us != None):
                raise UserExeception('Gmail đã tồn tại')
            db.add(User(IDUser = IDUser, Gmail = Gmail, Password = Password, QuyenUser = user.QuyenUser, ThoiGianDangKi = ThoiGianDangKi))
            db.commit()
            return user
    def SearchUserByGmail(self, Gmail: str):
        with SessionLocal() as db:
            res = []
            try:
                res = db.query(User).filter(User.Gmail.like('%'+Gmail+'%')).all()
                if(res == None):
                    return None
                listObject = []
                for row in res:
                    IDUser = row.IDUser
                    Gmail = row.Gmail
                    Password = row.Password
                    QuyenUser = row.QuyenUser
                    listObject.append({'IDUser': IDUser, 'Gmail': Gmail, 'Password': Password, 'QuyenUser': QuyenUser})
                return listObject
            except Exception as e:
                raise UserExeception(getattr(e, 'message', repr(e)))
    def GetPhanTramSoVoiThangTruoc(self):
        with SessionLocal() as db:
            percentage_change = 0
            try:
                last_month_count = db.query(User).filter(extract('month', User.ThoiGianDangKi) == extract('month', func.now()) - 1).count()
                this_month_count = db.query(User).filter(extract('month', User.ThoiGianDangKi) == extract('month', func.now())).count()
                if last_month_count == 0 and this_month_count > 0:
                    percentage_change = 100 * this_month_count
                elif last_month_count == 0 and this_month_count == 0:
                    percentage_change = 0
                else:
                    percentage_change = ((this_month_count - last_month_count) / last_month_count) * 100
                return percentage_change
            except Exception:
                raise UserExeception("Lấy phần trăm so với tháng trước thất bại")



