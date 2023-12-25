from fastapi import APIRouter, Request, status, Depends, Header, HTTPException, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from starlette.datastructures import URL
from App.Controllers.SiteController import *
from App.auth.jwt_bearer import jwtBearer
from App.auth.jwt_handler import decodeJWT
import js2py
import json
siteRouter = APIRouter()
siteController = SiteController()

@siteRouter.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return siteController.index(request)

#Trang chủ
@siteRouter.get("/{userID}", response_class=HTMLResponse)
async def index(request: Request, userID: str):
    return siteController.adminIndex(request, userID)

#chi tiết tuyển dụng
@siteRouter.get("/Chi-tiet-td/{IDTD}", response_class=HTMLResponse)
async def formChiTiet(request: Request, IDTD: str):
    return siteController.formChiTiet(request, IDTD)

#chi tiết tuyển dụng
@siteRouter.get("/{userID}/Chi-tiet-td/{IDTD}", response_class=HTMLResponse)
async def formChiTiet(request: Request, IDTD: str):
    return siteController.formChiTiet(request, IDTD)
#Chi tiết tuyển dụng khi tìm kiếm
@siteRouter.get("/{userID}/tim-kiem-DuLieu/{Text}/{LinhVucTD}/{DiaDiem}/Chi-tiet-td/{IDTD}", response_class=HTMLResponse)
async def formChiTietTimKiem(request: Request, IDTD: str):
    return siteController.formChiTiet(request, IDTD)
@siteRouter.get("/{userID}/danh-sach-tk", response_class=HTMLResponse)
async def danhsachtk(request: Request):
    return siteController.danhsachtk(request)

@siteRouter.get("/{userID}/TongQuan", response_class=HTMLResponse)
async def tongQuan(request: Request, userID: str):
    return siteController.TongQuan(request, userID)

@siteRouter.get("/{userID}/tim-kiem-DuLieu/{Text}/{LinhVucTD}/{DiaDiem}", response_class=HTMLResponse)
async def formTimKiem(request: Request, Text: str = None, LinhVucTD: str = None, DiaDiem: str = None, userID: str = None):
    return siteController.formTimKiem(request, Text, LinhVucTD, DiaDiem, userID)

@siteRouter.get("/{userID}/tim-kiem-DuLieu", response_class=HTMLResponse)
async def formTimKiem(request: Request, userID: str = None):
    return siteController.formTimKiem(request, None, None, None, userID)
#Trang admin tuyển dụng
@siteRouter.get("/{userID}/admin-Add-TD", response_class=HTMLResponse)
async def adminAddTD(request: Request, userID: str):
    return siteController.adminAddTD(request, userID)

#Trang cật nhật bài tuyển dụng của admin
@siteRouter.get("/{userID}/admin-Edit-TD/{IDTD}", response_class=HTMLResponse)
async def EditTDByID(request: Request, userID: str, IDTD: str):
    res = siteController.EditTDByID(request, userID, IDTD)
    if res == None:
        raise HTTPException(status_code=404, detail="Không tìm thấy ID bài tuyển dụng")
    return res

#Trang chủ chỉnh sửa tuyển dụng của admin
@siteRouter.get("/{userID}/admin-Edit-TD", response_class=HTMLResponse)
async def adminEditTD(request: Request, userID: str):
    return siteController.adminEditTD(request, userID)

#Kiểm tra đăng nhập thành công
@siteRouter.post("/CheckLoginSuccess/", response_class=HTMLResponse)
async def check_login_success(*, authorization: str = Form(), request: Request):
    try:
        if "Bearer " in authorization:
            token = json.loads(authorization.split("Bearer ")[1])["access token"]
            jwt_bearer = jwtBearer()
            payload = jwt_bearer.verify_jwt(token)
            if payload:
                return json.dumps(payload)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or token expired")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization header")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

#Giao diện trang chủ tùy theo loại người dùng
@siteRouter.post("/{userID}", response_class=HTMLResponse)
async def LoginSuccess(request: Request, token: str = Form()):
    try:
        token = json.loads(token)["access token"]
        jwt_bearer = jwtBearer()
        payload = jwt_bearer.verify_jwt(token)
        if payload:
            return siteController.LoginSuccess(request, payload["userType"], payload["userID"])
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or token expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
