from fastapi import APIRouter, Depends, HTTPException, status
from App.Model.UserModel import *
userRoute = APIRouter()
usermodel = UserModel()

@userRoute.get("/Users/")
async def GetAllUser():
    return usermodel.GetAllUser()

@userRoute.post("/Login/")
async def CheckLogin(user: UserLogin):
    return usermodel.CheckLogin(user.Gmail, user.Password)

@userRoute.post("/Register/")
async def Register(user: UserRegister):
    return usermodel.AddUser(user)

@userRoute.post("/ForgotPassword/")
async def ForgotPassword(Gmail: str = Form(...)):
    return usermodel.ForgotPassword(Gmail)