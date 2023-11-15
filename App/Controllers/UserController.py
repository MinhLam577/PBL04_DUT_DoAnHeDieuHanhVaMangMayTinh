from App.Model.UserModel import *
from router.UserRouter import *
class UserController:
    def __init__(self):
        self.UserModel = UserModel()
    def GetAllUser(self):
        return self.UserModel.GetAllUser()