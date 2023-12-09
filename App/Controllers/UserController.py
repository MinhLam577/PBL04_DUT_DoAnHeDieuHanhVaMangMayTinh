from App.Model.UserModel import *
from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory="App/View/templates")
class UserController:
    def __init__(self):
        self.UserModel = UserModel() 
    def GetAllUser(self):
        return self.UserModel.GetAllUser()
    def CheckLogin(self, Gmail, Password):
        return self.UserModel.CheckLogin(Gmail, Password)
    def ForgotPassword(self, Gmail):
        return self.UserModel.ForgotPassword(Gmail)
    def AddUser(self, user):
        return self.UserModel.AddUserRegister(user)
    def GetUserByGmail(self, Gmail):
        return self.UserModel.GetUserByGmail(Gmail)