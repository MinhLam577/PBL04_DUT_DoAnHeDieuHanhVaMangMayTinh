from App.Model.TDModel import *
class TDController:
    def __init__(self):
        self.TDModel = TDModel()
    def GetAllTDs(self):
        return self.TDModel.GetAllTD()
    def AddTD(self, td: TuyenDung):
        return self.TDModel.AddTD(td)
    def DeleteTD(self, IDTD: str):
        return self.TDModel.DeleteTD(IDTD)
    def UpdateTD(self, td: TuyenDung):
        return self.TDModel.UpdateTD(td)
    def GetTDByIDTD(self, IDTD: str):
        return self.TDModel.GetTDByIDTD(IDTD)
    def TimKiemTD(self, Text: str, LinhVucTD: str, DiaDiem: str):
        return self.TDModel.TimKiemTD(Text, LinhVucTD, DiaDiem)
    def TimKiemTDByID(self, IDTD: str):
        return self.TDModel.TimKiemTDByID(IDTD)
    def GetTDTuongTac(self):
        return self.TDModel.GetTDTuongTac()