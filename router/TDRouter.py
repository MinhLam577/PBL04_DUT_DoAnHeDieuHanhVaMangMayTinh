from fastapi import APIRouter, Depends, HTTPException, status, Body, Header
from typing import Optional
from App.Controllers.TDController import *
from fastapi.responses import RedirectResponse, HTMLResponse
from App.auth.jwt_handler import signJWT
from App.auth.jwt_bearer import jwtBearer
from App.auth.jwt_handler import decodeJWT
from datetime import date, datetime
import json
import random
tdRouter = APIRouter()
tdController = TDController()

#Lấy tất cả tuyển dụng
@tdRouter.get('/TDs/')
async def GetAllTDs():
    return tdController.GetAllTDs()

#Lấy tuyển dụng theo IDTD
@tdRouter.get("/TDs/{IDTD}")
async def GetTD(IDTD: str):
    td = tdController.GetTDByIDTD(IDTD)
    return td

#Thêm mới tuyển dụng
@tdRouter.post("/TDs/AddTD/")
async def AddTD(NoiTD: str = Form(None), NgayTD: datetime = Form(None), SoLuongTD: int = Form(None), LinhVucTD: str = Form(None), ViTriTD: str = Form(None), MoTaCongViec: str = Form(None), YeuCauCongViec: str = Form(None), QuyenLoi: str = Form(None), DiaDiem: str = Form(None), SDT: str = Form(None), Gmail: str = Form(None), LuongTD: str = Form(None), IDPost: str = Form(None)):
    try:
        listTD = tdController.GetAllTDs()
        listIDTD = [td["IDTD"] for td in listTD]
        IDTD = ""
        while(True):
            IDTD = "TD" + str(random.randint(1, 999999))
            if(IDTD not in listIDTD):
                break
        td = TuyenDung(IDTD=IDTD, NoiTD=NoiTD, NgayTD=NgayTD, SoLuongTD=SoLuongTD, LinhVucTD=LinhVucTD, ViTriTD=ViTriTD, MotaCongViec=MoTaCongViec, YeuCauCongViec=YeuCauCongViec, QuyenLoi=QuyenLoi, DiaDiem=DiaDiem, SDT=SDT, Gmail=Gmail, LuongTD=LuongTD, IDPost=IDPost)
        return tdController.AddTD(td)
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))

#Xóa tuyển dụng theo IDTD 
@tdRouter.delete("/TDs/DeleteTD/")
async def DeleteTD(IDTD: str = Form(...)):
    try:
        return tdController.DeleteTD(IDTD)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
#Cật nhật tuyển dụng theo IDTD
@tdRouter.put("/TDs/UpdateTD/")
async def UpdateTD(IDTD: str = Form(...), NoiTD: str = Form(None), NgayTD: datetime = Form(None), SoLuongTD: int = Form(None), LinhVucTD: str = Form(None), ViTriTD: str = Form(None), MoTaCongViec: str = Form(None), YeuCauCongViec: str = Form(None), QuyenLoi: str = Form(None), DiaDiem: str = Form(None), SDT: str = Form(None), Gmail: str = Form(None), LuongTD: str = Form(None), IDPost: str = Form(None)):
    try:
        td = TuyenDung(IDTD=IDTD, NoiTD=NoiTD, NgayTD=NgayTD, SoLuongTD=SoLuongTD, LinhVucTD=LinhVucTD, ViTriTD=ViTriTD, MotaCongViec=MoTaCongViec, YeuCauCongViec=YeuCauCongViec, QuyenLoi=QuyenLoi, DiaDiem=DiaDiem, SDT=SDT, Gmail=Gmail, LuongTD=LuongTD,IDPost=IDPost)
        return tdController.UpdateTD(td)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

#Tìm kiếm tuyển dụng
@tdRouter.post('/TDs/SearchTD/')
async def TimKiemTD(Text: str = Form(...), LinhVucTD: str = Form(...), DiaDiem: str = Form(...)):
    return tdController.TimKiemTD(Text, LinhVucTD, DiaDiem)

#Tìm kiếm tuyển dụng theo IDTD
@tdRouter.post('/TDs/SearchTDByID/')
async def TimKiemTDByID(IDTD: str = Form(None)):
    if IDTD is None:
        IDTD = ""
    return tdController.TimKiemTDByID(IDTD)