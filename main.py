import traceback
from router.indexRouter import *
from App.auth.jwt_handler import *
import datetime

import uvicorn
if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    except Exception:
        traceback.print_exc()