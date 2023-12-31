from fastapi import APIRouter, Depends, HTTPException, status, Body, Form
from App.Controllers.UserController import *
from fastapi.responses import RedirectResponse, HTMLResponse
from App.auth.jwt_handler import signJWT
import json
userRoute = APIRouter()
userController = UserController()

#Lấy tất cả user 
@userRoute.get("/Users/", name = "Lấy tất cả user")
async def GetAllUser():
    return userController.GetAllUser()

def CheckLogin(user: UserLogin):
    return userController.CheckLogin(user.Gmail, user.Password)

@userRoute.get("/Users/{Gmail}", name="Lấy user theo Gmail")
def GetUserByGmail(Gmail: str):
    return userController.GetUserByGmail(Gmail)

#Kiểm tra đăng nhập theo JWT handler
@userRoute.post("/CheckLoginJWT/", name="Kiểm tra đăng nhập bằng JWT")
async def LoginJWT(user: UserLogin):
    userType = CheckLogin(user)
    if(userType != None):
        return signJWT(user.Gmail, userType)

#API đăng kí tài khoản cho user
@userRoute.post("/Register/", name = "Đăng kí tài khoản user")
async def Register(user: UserRegister):
    return userController.AddUserRegister(user)

#API lấy lại mật khẩu theo gmail
@userRoute.post("/ForgotPassword/", name="Quên mật khẩu")
async def ForgotPassword(Gmail: str = Body(...)):
    return userController.ForgotPassword(Gmail)

#Thêm user
@userRoute.post("/Users/AddUser/", name="Thêm mới tài khoản user")
async def AddUser(user: UserAdd):
    try:
        return userController.AddUser(user)
    except UserExeception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        ) 

#Cật nhật user theo gmail
@userRoute.put("/Users/UpdateUser/", name="Cật nhật tài khoảng user")
async def UpdateUser(user: UserUpdate):
    try:
        return userController.UpdateUser(user)
    except UserExeception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        ) 

#Xóa user theo gmail
@userRoute.delete("/Users/DeleteUser/", name="Xóa tài khoản user")
async def DeleteUserByGmail(Gmail: str = Form(...)):
    return userController.DeleteUserByGmail(Gmail)

@userRoute.post("/Users/SearchUserByGmail", name="Tìm kiếm user theo gmail")
async def SearchUserByGmail(Gmail: str = Form(None)):
    if Gmail is None:
        Gmail = ""
    return userController.SearchUserByGmail(Gmail)