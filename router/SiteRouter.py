from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.datastructures import URL
from App.Controllers.SiteController import *

siteRouter = APIRouter()
siteController = SiteController()

@siteRouter.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return siteController.index(request)

@siteRouter.get("/Login/", response_class=HTMLResponse)
async def Login(request: Request):
    return siteController.Login(request)
@siteRouter.get("/Login/{userType}", response_class=HTMLResponse)
async def LoginSuccess(request: Request, userType: str | None = None):
    return siteController.LoginSuccess(request, userType)