from fastapi import APIRouter, Request, status, Depends, Header, HTTPException, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from typing import Annotated
from starlette.datastructures import URL
from App.Controllers.SiteController import *
from App.auth.jwt_bearer import jwtBearer
from App.auth.jwt_handler import decodeJWT
import json
siteRouter = APIRouter()
siteController = SiteController()

@siteRouter.get("/", response_class=HTMLResponse, name = "Giao diện đăng nhập")
async def login(request: Request):
    return siteController.index(request)

@siteRouter.get("/Login", response_class=HTMLResponse, name = "Giao diện đăng nhập")
async def login(request: Request):
    return siteController.Login(request)

@siteRouter.get("/{userID}", response_class=HTMLResponse, name = "Giao diện trang chủ admin khi đăng nhập thành công")
async def index(request: Request, userID: str):
    user = user_controller.GetUserByGmail(userID)
    if user is None:
        return RedirectResponse(url="/Login")
    if user.QuyenUser == "user":
        return siteController.LoginSuccess(request, "user", userID)
    else:
        return RedirectResponse(url="/admin/{userID}")

#Trang chủ admin
@siteRouter.get("/admin/{userID}", response_class=HTMLResponse, name = "Giao diện trang chủ admin khi đăng nhập thành công")
async def index(request: Request, userID: str):
    user = user_controller.GetUserByGmail(userID)
    if user is None:
        return RedirectResponse(url="/Login")
    if user.QuyenUser == "admin":
        return siteController.adminIndex(request, userID)
    return RedirectResponse(url="/Login")

#Chi tiết tuyển dụng theo userID
@siteRouter.get("/{userID}/Chi-tiet-td/{IDTD}", response_class=HTMLResponse, name = "Giao diện chi tiết tuyển dụng")
async def formChiTiet(request: Request, IDTD: str, userID: str):
    return siteController.formChiTiet(request, IDTD, userID)

#Chi tiết tuyển dụng của admin đã đăng nhập
@siteRouter.get("/admin/{userID}/Chi-tiet-td/{IDTD}", response_class=HTMLResponse, name = "Giao diện chi tiết tuyển dụng")
async def formChiTiet(request: Request, IDTD: str, userID: str = None):
    return siteController.formChiTiet(request, IDTD, userID)

#Chi tiết tuyển dụng khi không đăng nhập
@siteRouter.get("/Chi-tiet-td/{IDTD}", response_class=HTMLResponse, name = "Giao diện chi tiết tuyển dụng")
async def formChiTiet(request: Request, IDTD: str, userID: str = None):
    return siteController.formChiTiet(request, IDTD, userID)

@siteRouter.get("/{userID}/danh-sach-tk", response_class=HTMLResponse, name = "Giao diện danh sách tài khoản của admin")
async def danhsachtk(request: Request):
    return siteController.danhsachtk(request)

@siteRouter.get("/{userID}/TongQuan", response_class=HTMLResponse, name = "Giao diện tổng quan")
async def tongQuan(request: Request, userID: str):
    return siteController.TongQuan(request, userID)

#Tìm kiếm khi đã đăng nhập 
@siteRouter.get("/{userID}/tim-kiem-DuLieu/{Text}/{LinhVucTD}/{DiaDiem}", response_class=HTMLResponse, name = "Giao diện tìm kiếm có dữ liệu")
async def formTimKiem(request: Request, Text: str = None, LinhVucTD: str = None, DiaDiem: str = None, userID: str = None):
    return siteController.formTimKiem(request, Text, LinhVucTD, DiaDiem, userID)

#Chi tiết tuyển dụng của admin đã đăng nhập
@siteRouter.get("/admin/{userID}/tim-kiem-DuLieu/{Text}/{LinhVucTD}/{DiaDiem}", response_class=HTMLResponse, name = "Giao diện chi tiết tuyển dụng")
async def formTimKiem(request: Request, Text: str = None, LinhVucTD: str = None, DiaDiem: str = None, userID: str = None):
    return siteController.formTimKiem(request, Text, LinhVucTD, DiaDiem, userID)

#Tìm kiếm khi chưa đăng nhập
@siteRouter.get("/tim-kiem-DuLieu/{Text}/{LinhVucTD}/{DiaDiem}", response_class=HTMLResponse, name = "Giao diện tìm kiếm có dữ liệu")
async def formTimKiem(request: Request, Text: str = None, LinhVucTD: str = None, DiaDiem: str = None, userID: str = None):
    return siteController.formTimKiem(request, Text, LinhVucTD, DiaDiem, userID)

#Tìm kiếm của admin khi không có dữ liệu
@siteRouter.get("/{userID}/tim-kiem-DuLieu", response_class=HTMLResponse, name="Giao diện tìm kiếm không có dữ liệu")
async def formTimKiem(request: Request, userID: str = None):
    return siteController.formTimKiem(request, None, None, None, userID)

#Trang admin tuyển dụng
@siteRouter.get("/{userID}/admin-Add-TD", response_class=HTMLResponse, name="Giao diện thêm tuyển dụng")
async def adminAddTD(request: Request, userID: str):
    return siteController.adminAddTD(request, userID)

#Trang cật nhật bài tuyển dụng của admin
@siteRouter.get("/{userID}/admin-Edit-TD/{IDTD}", response_class=HTMLResponse, name="Giao diện cật nhật tuyển dụng theo IDTD")
async def EditTDByID(request: Request, userID: str, IDTD: str):
    res = siteController.EditTDByID(request, userID, IDTD)
    if res == None:
        return JSONResponse(
            content={"message": "Không tìm thấy bài tuyển dụng"}
        )
    return res

#Trang chủ chỉnh sửa tuyển dụng của admin
@siteRouter.get("/{userID}/admin-Edit-TD", response_class=HTMLResponse, name = "Giao diện quản lí tuyển dụng của admin")
async def adminEditTD(request: Request, userID: str):
    return siteController.adminEditTD(request, userID)

#Kiểm tra đăng nhập thành công
@siteRouter.post("/CheckLoginSuccess/", response_class=HTMLResponse, name = "Kiểm tra đăng nhập thành công và xác thực token")
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
@siteRouter.post("/{userID}", response_class=HTMLResponse, name= "Giao diện trang chủ tùy theo loại người dùng")
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
