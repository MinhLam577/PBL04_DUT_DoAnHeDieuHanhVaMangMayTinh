from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from App.Controllers.SiteController import *

siteRouter = APIRouter()
siteController = SiteController()
@siteRouter.get("/Login/", response_class=HTMLResponse)
async def Home(request: Request):
    return siteController.Home(request)

@siteRouter.get("/Admin/", response_class=HTMLResponse)
async def Admin(request: Request):
    return siteController.Admin(request)

@siteRouter.get("/User/", response_class=HTMLResponse)
async def User(request: Request):
    return siteController.User(request)