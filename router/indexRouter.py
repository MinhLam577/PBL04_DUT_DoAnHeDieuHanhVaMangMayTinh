from router.UserRouter import *
from router.SiteRouter import *
from router.PostRouter import *
from router.TuongTacRouter import *
from router.TDRouter import *
from config.app import app
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="App/View/static", html=True), name="static")
@app.exception_handler(UserExeception)
async def unicorn_exception_handler(request: Request, exc: UserExeception):
    return JSONResponse(
        content={"message": exc.message},
    )
@app.exception_handler(PostException)
async def unicorn_exception_handler(request: Request, exc: PostException):
    return JSONResponse(
        content={"message": exc.message},
    )
@app.exception_handler(TDException)
async def unicorn_exception_handler(request: Request, exc: TDException):
    return JSONResponse(
        content={"message": exc.message},
    )
@app.exception_handler(TuongTacException)
async def unicorn_exception_handler(request: Request, exc: TuongTacException):
    return JSONResponse(
        content={"message": exc.message},
    )
app.include_router(siteRouter)
app.include_router(userRoute)
app.include_router(PostRouter)
app.include_router(tdRouter)
app.include_router(ttRouter)

    