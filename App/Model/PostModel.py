from config.db import SessionLocal
from pydantic import BaseModel, validator
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import Request, Depends, Form
from App.Model.PostEntity import *
class PostException(Exception):
    def __init__(self, message: str):
        self.message = message
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
class PostModel:
    def AddPost(self, post: Post):
        with SessionLocal() as db:
            try:
                db.add(post)
                db.commit()
                return True
            except Exception:
                raise PostException("Thêm bài viết thất bại")
    def GetAllPost(self):
        with SessionLocal() as db:
            listPost = db.query(Post).all()
            listPostConvert = []
            for post in listPost:
                IDPost = post.IDPost
                TimePost = post.TimePost
                ContentPost = post.ContentPost
                LinkPost = post.LinkPost
                LinkImg = post.LinkImg
                listPostConvert.append({"IDPost": IDPost, "TimePost": TimePost, "ContentPost": ContentPost, "LinkPost": LinkPost, "LinkImg": LinkImg})
            return listPostConvert
    def GetAllContentPost(self):
        with SessionLocal() as db:
            listPost = db.query(Post.ContentPost).all()
            listPost = [post.ContentPost for post in listPost]
            return listPost
    def GetAllIDPost(self):
        with SessionLocal() as db:
            listPost = db.query(Post.IDPost).all()
            listPost = [post.IDPost for post in listPost]
            return listPost
    def DeletePostByIDPost(self, IDPost: str):
        with SessionLocal() as db:
            try:
                db.query(Post).filter(Post.IDPost == IDPost).delete()
                db.commit()
                return True
            except Exception as e:
                raise PostException(getattr(e, 'message', repr(e)))
    def DeleteDuplicatePost(self):
        with SessionLocal() as db:
            try:
                db.execute(text("CALL `DeleteDuplicatePosts`()"))
                db.commit()
                return True
            except Exception:
                raise PostException("Xóa bài viết trùng lặp thất bại")
