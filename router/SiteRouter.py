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

#Trang chủ
@siteRouter.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return siteController.index(request)
@siteRouter.get("/LoginSuccess/index", response_class=HTMLResponse)

#Trang chủ admin
async def index(request: Request):
    return siteController.adminIndex(request)

#Thêm tuyển dụng của admin
@siteRouter.get("/admin/Add-New-TD", response_class=HTMLResponse)
async def index_admin(request: Request):
    return siteController.index_admin(request)

#Trang admin tuyển dụng
@siteRouter.get("/LoginSuccess/adminTuyenDung", response_class=HTMLResponse)
async def adminTuyenDung(request: Request):
    return siteController.adminTuyenDung(request)

#Trang chỉnh sửa tuyển dụng của admin
@siteRouter.get("/LoginSuccess/admin-Edit-TD", response_class=HTMLResponse)
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
                redirectUrl = request.url_for("LoginSuccess", token=token)
                return RedirectResponse(url=redirectUrl, status_code=status.HTTP_303_SEE_OTHER)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or token expired")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization header")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

#Giao diện trang chủ tùy theo loại người dùng
@siteRouter.get("/LoginSuccess/{token}", response_class=HTMLResponse, name="LoginSuccess")
async def LoginSuccess(request: Request, token: str | None = None):
    jwt_bearer = jwtBearer()
    token= json.loads(token)["access token"]
    payload = jwt_bearer.verify_jwt(token)
    if payload:
        return siteController.LoginSuccess(request, payload["userType"])
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or token expired")
