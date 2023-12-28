from fastapi import APIRouter, Depends, HTTPException, status, Body, Form
from App.Controllers.TuongTacController import *
from fastapi.responses import RedirectResponse, HTMLResponse
from App.auth.jwt_handler import signJWT
import json

ttRouter = APIRouter()
ttController = TuongTacController()

@ttRouter.post("/TuongTac/AddTT/", name="Thêm mới tương tác")
async def AddTT(tt: TuongTacAdd):
    try:
        return ttController.AddTT(tt)
    except TuongTacException as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        )
    except Exception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        )

@ttRouter.delete("/TuongTac/DeleteTT/", name="Xóa tương tác")
async def DelTT(tt: TuongTacDel):
    try:
        return ttController.DeleteTT(tt)
    except Exception as e:
        return JSONResponse(
            content={"message": getattr(e, 'message', repr(e))},
        )