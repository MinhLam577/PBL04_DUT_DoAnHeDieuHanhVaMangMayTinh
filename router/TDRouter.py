from fastapi import APIRouter, Depends, HTTPException, status, Body
from App.Controllers.TDController import *
from fastapi.responses import RedirectResponse, HTMLResponse
from App.auth.jwt_handler import signJWT
tdRouter = APIRouter()
tdController = TDController()

@tdRouter.get('/TDs/')
async def GetAllTDs():
    return tdController.GetAllTDs()