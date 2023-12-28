from App.Model.TuongTacModel import *
from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory="App/View/templates")
class TuongTacController:
    def __init__(self):
        self.TuongTacModel = TuongTacModel()
    def AddTT(self, tt: TuongTacAdd):
        return self.TuongTacModel.AddTT(tt)
    def DeleteTT(self, tt: TuongTacDel):
        return self.TuongTacModel.DeleteTT(tt)
    