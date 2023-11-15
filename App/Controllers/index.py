from App.Controllers.UserController import *
from App.Controllers.PostController import *
from config.app import app
app.include_router(userRoute)
@app.exception_handler(UvicornExeception)
async def unicorn_exception_handler(request: Request, exc: UvicornExeception):
    return JSONResponse(
        content={"message": exc.message},
    )
class index:
    def __init__(self):
        self.UserController = UserController()
        