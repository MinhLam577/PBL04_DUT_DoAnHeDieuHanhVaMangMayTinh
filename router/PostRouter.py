from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import RedirectResponse
from App.Controllers.PostController import *
from App.auth.jwt_bearer import jwtBearer
PostRouter = APIRouter()
PostController = PostControllers()

@PostRouter.get("/GetAllPost/", dependencies=[Depends(jwtBearer())], name="Lấy tất cả bài viết")
async def GetAllPost():
    return PostController.GetAllPost()
