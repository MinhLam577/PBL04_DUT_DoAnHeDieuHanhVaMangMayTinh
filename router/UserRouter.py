from fastapi import APIRouter, Depends, HTTPException, status, Body
from App.Controllers.UserController import *
from fastapi.responses import RedirectResponse, HTMLResponse
from App.auth.jwt_handler import signJWT
userRoute = APIRouter()
userController = UserController()

@userRoute.get("/Users/")
async def GetAllUser():
    return userController.GetAllUser()

def CheckLogin(user: UserLogin):
    return userController.CheckLogin(user.Gmail, user.Password)

@userRoute.post("/CheckLoginJWT/")
async def LoginJWT(user: UserLogin):
    userType = CheckLogin(user)
    if(userType != None):
        return signJWT(user.Gmail, userType)

@userRoute.post("/Register/")
async def Register(user: UserRegister):
    return userController.AddUser(user)

@userRoute.post("/ForgotPassword/")
async def ForgotPassword(Gmail: str = Body(...)):
    return userController.ForgotPassword(Gmail)


