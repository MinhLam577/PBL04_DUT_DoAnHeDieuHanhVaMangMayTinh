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
@siteRouter.get("/{userID}/index", response_class=HTMLResponse)
async def index(request: Request):
    return siteController.adminIndex(request)

@siteRouter.get("/{userID}/TongQuan", response_class=HTMLResponse)
async def tongQuan(request: Request):
    return siteController.TongQuan(request)

#Trang admin tuyển dụng
@siteRouter.get("/{userID}/adminTuyenDung", response_class=HTMLResponse)
async def adminTuyenDung(request: Request):
    return siteController.adminTuyenDung(request)

#Trang chỉnh sửa tuyển dụng của admin
@siteRouter.get("/{userID}/admin-Edit-TD", response_class=HTMLResponse)
async def adminEditTD(request: Request):
    return siteController.adminEditTD(request)

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
