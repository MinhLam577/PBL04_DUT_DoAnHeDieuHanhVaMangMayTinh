from App.Model.TDModel import *
class TDController:
    def __init__(self):
        self.TDModel = TDModel()
    def GetAllTDs(self):
        return self.TDModel.GetAllTD()
    def AddTD(self, td: TuyenDung):
        return self.TDModel.AddTD(td)