from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import RedirectResponse
from App.Controllers.PostController import *
PostRouter = APIRouter()
PostController = PostControllers()

@PostRouter.post("/AddPost/")
async def AddPost(post: Post):
    return PostController.AddPost(post)

@PostRouter.get("/GetAllPost/")
async def GetAllPost():
    return PostController.GetAllPost()
