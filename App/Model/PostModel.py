from App.Model.UserEntity import User, Base
from config.db import SessionLocal, engine
from pydantic import BaseModel, validator
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import Request, Depends, Form