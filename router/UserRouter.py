from fastapi import APIRouter, Depends, HTTPException, status, Body
from App.Controllers.UserController import *
from fastapi.responses import RedirectResponse, HTMLResponse
from App.auth.jwt_handler import signJWT
userRoute = APIRouter()
userController = UserController()

@userRoute.get("/Users/")
async def GetAllUser():
    return userController.GetAllUser()

def CheckLoginJWT(user: UserLogin):
    if(userController.CheckLogin(user.Gmail, user.Password) != None):
        return True
    else:
        return False

@userRoute.post("/CheckLoginJWT/")
async def LoginJWT(user: UserLogin):
    if(CheckLoginJWT(user) == True):
        return signJWT(user.Gmail)
    
@userRoute.post("/SingUpJWT/")
async def SingUpJWT(user: UserRegister):
    return signJWT(user.Gmail)


@userRoute.post("/CheckLogin/")
async def CheckLogin(user: UserLogin):
    userType = userController.CheckLogin(user.Gmail, user.Password)
    if(userType != None):   
        return userType

@userRoute.post("/Register/")
async def Register(user: UserRegister):
    return userController.AddUser(user)
        

@userRoute.post("/ForgotPassword/")
async def ForgotPassword(Gmail: str = Body(...)):
    return userController.ForgotPassword(Gmail)


