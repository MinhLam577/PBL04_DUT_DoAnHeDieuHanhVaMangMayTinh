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

#Cật nhật user theo gmail
@userRoute.put("/Users/UpdateUser/")
async def UpdateUser(IDUser: str = Body(...), user: UserUpdate = Body(...)):
    user = dict(exclude_unset=True, **user)
    return userController.UpdateUser(IDUser, user)

#Xóa user theo gmail
@userRoute.delete("/Users/DeleteUser/")
async def DeleteUserByGmail(Gmail: str = Body(...)):
    return userController.DeleteUserByGmail(Gmail)

