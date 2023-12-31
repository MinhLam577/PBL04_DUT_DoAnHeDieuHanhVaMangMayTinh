from fastapi import APIRouter, Depends, HTTPException, status, Body, Header, File, UploadFile
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
@tdRouter.get('/TDs/', name="Lấy tất cả bài tuyển dụng", dependencies=[Depends(jwtBearer())])
async def GetAllTDs(request: Request):
    try:
        authorization = request.headers.get('Authorization')
        if "Bearer " in authorization:
            token = json.loads(authorization.split("Bearer ")[1])["access token"]
            jwt_bearer = jwtBearer()
            payload = jwt_bearer.verify_jwt(token)
            if payload:
                userType = payload["userType"]
                if(userType == "admin"):
                    return tdController.GetAllTDs()
                else:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token không hợp lệ hoặc đã hết hạn")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Header xác thực không hợp lệ")
    except Exception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        )

#Lấy tuyển dụng theo IDTD
@tdRouter.get("/TDs/{IDTD}", name="Lấy tuyển dụng theo IDTD", dependencies=[Depends(jwtBearer())])
async def GetTD(IDTD: str, request: Request):
    try:
        authorization = request.headers.get('Authorization')
        if "Bearer " in authorization:
            token = json.loads(authorization.split("Bearer ")[1])["access token"]
            if(token == None):
                return tdController.GetTDByIDTD(IDTD)
            jwt_bearer = jwtBearer()
            payload = jwt_bearer.verify_jwt(token)
            if payload:
                return tdController.GetTDByIDTD(IDTD)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token không hợp lệ")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Header xác thực không hợp lệ")
    except Exception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        )

#Thêm mới tuyển dụng
@tdRouter.post("/TDs/AddTD/", name="Thêm mới tuyển dụng")
async def AddTD(NoiTD: str = Form(None), NgayTD: datetime = Form(None), SoLuongTD: str = Form(None), LinhVucTD: str = Form(None), ViTriTD: str = Form(None), MoTaCongViec: str = Form(None), YeuCauCongViec: str = Form(None), QuyenLoi: str = Form(None), DiaDiem: str = Form(None), SDT: str = Form(None), Gmail: str = Form(None), LuongTD: str = Form(None), IDPost: str = Form(None), image: UploadFile = File(None)):
    try:
        listTD = tdController.GetAllTDs()
        listIDTD = [td["IDTD"] for td in listTD]
        IDTD = ""
        while(True):
            IDTD = "TD" + str(random.randint(1, 999999))
            if(IDTD not in listIDTD):
                break
        td = TuyenDung(IDTD=IDTD, NoiTD=NoiTD, NgayTD=NgayTD, SoLuongTD=SoLuongTD, LinhVucTD=LinhVucTD, ViTriTD=ViTriTD, MotaCongViec=MoTaCongViec, YeuCauCongViec=YeuCauCongViec, QuyenLoi=QuyenLoi, DiaDiem=DiaDiem, SDT=SDT, Gmail=Gmail, LuongTD=LuongTD, IDPost=IDPost)
        return await tdController.AddTD(td, image)
    except Exception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        )

#Xóa tuyển dụng theo IDTD 
@tdRouter.delete("/TDs/DeleteTD/", name="Xóa tuyển dụng theo IDTD")
async def DeleteTD(IDTD: str = Form(...)):
    try:
        return tdController.DeleteTD(IDTD)
    except Exception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        )
    
#Cật nhật tuyển dụng theo IDTD
@tdRouter.put("/TDs/UpdateTD/", name="Cật nhật tuyển dụng theo IDTD")
async def UpdateTD(IDTD: str = Form(), NoiTD: str = Form(None), NgayTD: datetime = Form(None), SoLuongTD: str = Form(None), LinhVucTD: str = Form(None), ViTriTD: str = Form(None), MoTaCongViec: str = Form(None), YeuCauCongViec: str = Form(None), QuyenLoi: str = Form(None), DiaDiem: str = Form(None), SDT: str = Form(None), Gmail: str = Form(None), LuongTD: str = Form(None), IDPost: str = Form(None), image: UploadFile = File(None)):
    try:
        td = TuyenDung(IDTD=IDTD, NoiTD=NoiTD, NgayTD=NgayTD, SoLuongTD=SoLuongTD, LinhVucTD=LinhVucTD, ViTriTD=ViTriTD, MotaCongViec=MoTaCongViec, YeuCauCongViec=YeuCauCongViec, QuyenLoi=QuyenLoi, DiaDiem=DiaDiem, SDT=SDT, Gmail=Gmail, LuongTD=LuongTD,IDPost=IDPost)
        return await tdController.UpdateTD(td, image)
    except Exception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        )

#Tìm kiếm tuyển dụng theo IDTD
@tdRouter.post('/TDs/SearchTDByID/', name="Tìm kiếm tuyển dụng theo IDTD")
async def TimKiemTDByID(IDTD: str = Form(None)):
    if IDTD is None:
        IDTD = ""
    return tdController.TimKiemTDByID(IDTD)

@tdRouter.post("/TDs/ListUserTTByIDTD/", name="Tìm kiếm danh sách người dùng tương tác theo IDTD")
async def GetListUserTuongTacByIDTD(IDTD: str = Form(...), userID: str = Form(...)):
     return RedirectResponse(url=f"/{userID}/danh-sach-QuanTam/{IDTD}", status_code=303)
 
@tdRouter.post("/TDs/SearchUserByGmailAndIDTD", name="Tìm kiếm user theo gmail và IDTD")
async def SearchUserByGmailAndIDTD(Gmail: str = Form(None), IDTD: str = Form(...)):
    if Gmail is None:
        Gmail = ""
    return tdController.SearchUserByGmailAndIDTD(Gmail, IDTD)

@tdRouter.post("/TDs/SendGmail/", name = "Gửi gmail")
async def SendGmail(IDTD: str = Form(...)):
    try:
        tdController.SendGmail(IDTD)
        return True
    except Exception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        )
   