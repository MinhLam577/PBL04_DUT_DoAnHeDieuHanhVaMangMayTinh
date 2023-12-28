import traceback
from router.indexRouter import *
from App.auth.jwt_handler import *
from App.Controllers.TDController import TDController
import uvicorn
if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="localhost", port=6789, reload=True)
    except Exception:
        traceback.print_exc()