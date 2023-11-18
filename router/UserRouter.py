from fastapi import APIRouter, Depends, HTTPException, status, Body
from App.Controllers.UserController import *
from fastapi.responses import RedirectResponse, HTMLResponse
userRoute = APIRouter()
userController = UserController()

@userRoute.get("/Users/")
async def GetAllUser():
    return userController.GetAllUser()

@userRoute.post("/CheckLogin/")
async def CheckLogin(user: UserLogin, request: Request):
    userType = userController.CheckLogin(user.Gmail, user.Password)
    if(userType != None):   
        return userType
@userRoute.post("/Register/")
async def Register(user: UserRegister):
    return userController.AddUser(user)

@userRoute.post("/ForgotPassword/")
async def ForgotPassword(Gmail: str = Body(...)):
    return userController.ForgotPassword(Gmail)


