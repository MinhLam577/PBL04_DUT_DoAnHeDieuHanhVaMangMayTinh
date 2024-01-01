import traceback
from router.indexRouter import *
from App.auth.jwt_handler import *
import uvicorn
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment
if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="localhost", port=6789, reload=True)
    except Exception:
        traceback.print_exc()