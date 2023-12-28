from App.Model.UserModel import *
from fastapi.templating import Jinja2Templates
from App.Controllers.TuongTacController import TuongTacController
template = Jinja2Templates(directory="App/View/templates")
class UserController:
    def __init__(self):
        self.UserModel = UserModel() 
    def GetAllUser(self):
        return self.UserModel.GetAllUser()
    def GetUserByGmail(self, Gmail: str):
        return self.UserModel.GetUserByGmail(Gmail)
    def CheckLogin(self, Gmail, Password):
        return self.UserModel.CheckLogin(Gmail, Password)
    def ForgotPassword(self, Gmail):
        return self.UserModel.ForgotPassword(Gmail)
    def AddUser(self, user: UserAdd):
        return self.UserModel.AddUser(user)
    def AddUserRegister(self, user):
        return self.UserModel.AddUserRegister(user)
    def DeleteUserByGmail(self, Gmail: str):
        return self.UserModel.DeleteUserByGmail(Gmail)
    def UpdateUser(self, user: UserUpdate):
        return self.UserModel.UpdateUser(user)
    def SearchUserByGmail(self, Gmail: str):
        return self.UserModel.SearchUserByGmail(Gmail)
    def GetPhanTramSoVoiThangTruoc(self):
        return self.UserModel.GetPhanTramSoVoiThangTruoc()