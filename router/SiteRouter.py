from fastapi import APIRouter, Request, status, Depends, Header, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from starlette.datastructures import URL
from App.Controllers.SiteController import *
from App.auth.jwt_bearer import jwtBearer
from App.auth.jwt_handler import decodeJWT
import json
siteRouter = APIRouter()
siteController = SiteController()

@siteRouter.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return siteController.index(request)

@siteRouter.get("/Login/", response_class=HTMLResponse)
async def Login(request: Request):
    return siteController.Login(request)

@siteRouter.post("/CheckLoginSuccess/", response_class=HTMLResponse, dependencies=[Depends(jwtBearer())])
async def check_login_success(*,authorization: str = Header(None), request: Request):
    try:
        if "Bearer " in authorization:
            token =  json.loads(authorization.split("Bearer ")[1])["access token"]
            jwt_bearer = jwtBearer()
            payload = jwt_bearer.verify_jwt(token)
            if payload:
                userType = payload["userType"]
                return userType
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or token expired")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization header")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@siteRouter.get("/Login/{userType}", response_class=HTMLResponse)
async def LoginSuccess(request: Request, userType: str | None = None):
    return siteController.LoginSuccess(request, userType)