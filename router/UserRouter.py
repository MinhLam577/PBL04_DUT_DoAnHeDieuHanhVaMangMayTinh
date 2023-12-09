from fastapi import APIRouter, Depends, HTTPException, status, Body
from App.Controllers.UserController import *
from fastapi.responses import RedirectResponse, HTMLResponse
from App.auth.jwt_handler import signJWT
import json
userRoute = APIRouter()
userController = UserController()

#Lấy tất cả user 
@userRoute.get("/Users/")
async def GetAllUser():
    return userController.GetAllUser()

def CheckLogin(user: UserLogin):
    return userController.CheckLogin(user.Gmail, user.Password)

#Kiểm tra đăng nhập theo JWT handler
@userRoute.post("/CheckLoginJWT/")
async def LoginJWT(user: UserLogin):
    userType = CheckLogin(user)
    if(userType != None):
        return signJWT(user.Gmail, userType)

#API đăng kí tài khoản cho user
@userRoute.post("/Register/")
async def Register(user: UserRegister):
    return userController.AddUser(user)

#API lấy lại mật khẩu theo gmail
@userRoute.post("/ForgotPassword/")
async def ForgotPassword(Gmail: str = Body(...)):
    return userController.ForgotPassword(Gmail)

@userRoute.post("/Get-User-By-Gmail/")
async def GetUserByGmail(userGmail: str):
    us = userController.GetUserByGmail(userGmail)
    if(us == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gmail không tồn tại")
    else:
        return us


