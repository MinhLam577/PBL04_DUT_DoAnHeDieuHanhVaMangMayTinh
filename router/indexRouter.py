from router.UserRouter import *
from router.SiteRouter import *
from config.app import app
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="App/View/static", html=True), name="static")

@app.exception_handler(UserExeception)
async def unicorn_exception_handler(request: Request, exc: UserExeception):
    return JSONResponse(
        content={"message": exc.message},
    )
app.include_router(siteRouter)
app.include_router(userRoute)


    