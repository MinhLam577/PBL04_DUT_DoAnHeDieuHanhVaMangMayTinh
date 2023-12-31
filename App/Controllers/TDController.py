from App.Model.TDModel import *
class TDController:
    def __init__(self):
        self.TDModel = TDModel()
    def GetAllTDs(self):
        return self.TDModel.GetAllTD()
    async def AddTD(self, td: TuyenDung, image: UploadFile):
        return await self.TDModel.AddTD(td, image)
    def DeleteTD(self, IDTD: str):
        return self.TDModel.DeleteTD(IDTD)
    async def UpdateTD(self, td: TuyenDung, image: UploadFile):
        return await self.TDModel.UpdateTD(td, image)
    def GetTDByIDTD(self, IDTD: str):
        return self.TDModel.GetTDByIDTD(IDTD)
    def TimKiemTD(self, Text: str, LinhVucTD: str, DiaDiem: str, LuongTD: str):
        return self.TDModel.TimKiemTD(Text, LinhVucTD, DiaDiem, LuongTD)
    def TimKiemTDByID(self, IDTD: str):
        return self.TDModel.TimKiemTDByID(IDTD)
    def GetTDTuongTac(self):
        return self.TDModel.GetTDTuongTac()
    def GetListUserTuongTacByIDTD(self, IDTD: str):
        return self.TDModel.GetListUserTuongTacByIDTD(IDTD)
    def SearchUserByGmailAndIDTD(self, Gmail: str, IDTD: str):
        return self.TDModel.SearchUserByGmailAndIDTD(Gmail, IDTD)
    def SendGmail(self, IDTD: str):
        self.TDModel.SendGmail(IDTD)