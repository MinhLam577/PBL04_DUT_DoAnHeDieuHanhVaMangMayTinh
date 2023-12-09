from fastapi import APIRouter, Depends, HTTPException, status, Body, Header
from App.Controllers.TDController import *
from fastapi.responses import RedirectResponse, HTMLResponse
from App.auth.jwt_handler import signJWT
from App.auth.jwt_bearer import jwtBearer
from App.auth.jwt_handler import decodeJWT
import json
tdRouter = APIRouter()
tdController = TDController()

@tdRouter.get('/TDs/')
async def GetAllTDs():
    return tdController.GetAllTDs()

@tdRouter.put("/TDs/{IDTD}", dependencies=[Depends(jwtBearer())])
async def DeleteTD(IDTD: str, authorization: str = Header(None),):
    try:
        if "Bearer " in authorization:
            token =  json.loads(authorization.split("Bearer ")[1])["access token"]
            jwt_bearer = jwtBearer()
            payload = jwt_bearer.verify_jwt(token)
            if payload:
                return payload["userType"]
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or token expired")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization header")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))