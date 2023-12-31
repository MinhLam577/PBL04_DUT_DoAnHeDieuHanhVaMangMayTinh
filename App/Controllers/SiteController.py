from fastapi.templating import Jinja2Templates
from App.Controllers.TDController import TDController
from App.Controllers.UserController import UserController
from App.Controllers.TuongTacController import TuongTacController
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
template = Jinja2Templates(directory="App/View/templates")
tdController = TDController()
user_controller = UserController()
tt_Controller = TuongTacController()
class SiteController:
    def index(self, request):
        listTD = tdController.GetAllTDs()
        listTD = sorted(listTD, key=lambda x: datetime.strptime(str(x['NgayTD']), '%Y-%m-%d %H:%M:%S'), reverse=True)
        one_month_ago = datetime.now() - relativedelta(months=1)
        listTD = [td for td in listTD if datetime.strptime(str(td['NgayTD']), '%Y-%m-%d %H:%M:%S') > one_month_ago]
        LinhVucTD = [td['LinhVucTD'] for td in listTD]
        LinhVucTD = list(set(LinhVucTD))
        ViTriTD = [td['ViTriTD'] for td in listTD]
        ViTriTD = list(set(ViTriTD))
        NoiTD = [td['NoiTD'] for td in listTD]
        NoiTD = list(set(NoiTD))
        YeuCauCongViec = [td['YeuCauCongViec'] for td in listTD]
        YeuCauCongViec = list(set(YeuCauCongViec))
        DiaDiem = [
        "An Giang","Bà Rịa - Vũng Tàu","Bắc Giang","Bắc Kạn","Bạc Liêu","Bắc Ninh","Bến Tre","Bình Định","Bình Dương","Bình Phước","Bình Thuận","Cà Mau","Cần Thơ","Cao Bằng","Đà Nẵng", "Đắk Lắk","Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",  "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum" "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình","Thái Nguyên","Thanh Hóa","Thừa Thiên Huế","Tiền Giang","Thành phố Hồ Chí Minh","Trà Vinh","Tuyên Quang","Vĩnh Long","Vĩnh Phúc","Yên Bái"
        ]
        return template.TemplateResponse("index.html", {"request": request, 'listTD': listTD, 'LinhVucTD': LinhVucTD, 'DiaDiem': DiaDiem, 'ViTriTD': ViTriTD, 'NoiTD': NoiTD, 'YeuCauCongVIec': YeuCauCongViec})
    def Login(self, request):
        return template.TemplateResponse("login.html", {"request": request})
    def adminIndex(self, request, userID: str):
        listTD = tdController.GetAllTDs()
        listTD = sorted(listTD, key=lambda x: datetime.strptime(str(x['NgayTD']), '%Y-%m-%d %H:%M:%S'), reverse=True)
        one_month_ago = datetime.now() - relativedelta(months=1)
        listTD = [td for td in listTD if datetime.strptime(str(td['NgayTD']), '%Y-%m-%d %H:%M:%S') > one_month_ago]
        LinhVucTD = [td['LinhVucTD'] for td in listTD]
        LinhVucTD = list(set(LinhVucTD))
        ViTriTD = [td['ViTriTD'] for td in listTD]
        ViTriTD = list(set(ViTriTD))
        NoiTD = [td['NoiTD'] for td in listTD]
        NoiTD = list(set(NoiTD))
        YeuCauCongViec = [td['YeuCauCongViec'] for td in listTD]
        YeuCauCongViec = list(set(YeuCauCongViec))
        DiaDiem = [
        "An Giang","Bà Rịa - Vũng Tàu","Bắc Giang","Bắc Kạn","Bạc Liêu","Bắc Ninh","Bến Tre","Bình Định","Bình Dương","Bình Phước","Bình Thuận","Cà Mau","Cần Thơ","Cao Bằng","Đà Nẵng", "Đắk Lắk","Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",  "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum" "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình","Thái Nguyên","Thanh Hóa","Thừa Thiên Huế","Tiền Giang","Thành phố Hồ Chí Minh","Trà Vinh","Tuyên Quang","Vĩnh Long","Vĩnh Phúc","Yên Bái"
        ]
        return template.TemplateResponse("index.html", {"request": request, 'userID':userID, 'listTD': listTD, 'LinhVucTD': LinhVucTD, 'DiaDiem': DiaDiem, 'ViTriTD': ViTriTD, 'NoiTD': NoiTD, 'userType': "admin", 'YeuCauCongViec': YeuCauCongViec})
    def adminEditTD(self, request, userID: str):
        listTD = tdController.GetAllTDs()
        listTD = sorted(listTD, key=lambda x: datetime.strptime(str(x['NgayTD']), '%Y-%m-%d %H:%M:%S'), reverse=True)
        return template.TemplateResponse("formSuaXoaTD.html", {"request": request, 'userID': userID, 'listTD': listTD})
    def EditTDByID(self, request, userID: str, IDTD: str):
        td = tdController.GetTDByIDTD(IDTD)
        if td is None:
            return None
        return template.TemplateResponse("adminEditTD.html", {"request": request, 'userID': userID, 'td': td})
    def adminAddTD(self, request, userID: str):
        return template.TemplateResponse("adminAddTD.html", {"request": request, 'userID': userID})
    def LoginSuccess(self, request, userType: str | None = None, userID: str | None = None):
        if(userType == 'admin'):
            return template.TemplateResponse("adminIndex.html", {"request": request, 'userID' : userID})
        else:
            listTD = tdController.GetAllTDs()
            listTD = sorted(listTD, key=lambda x: datetime.strptime(str(x['NgayTD']), '%Y-%m-%d %H:%M:%S'), reverse=True)
            one_month_ago = datetime.now() - relativedelta(months=1)
            listTD = [td for td in listTD if datetime.strptime(str(td['NgayTD']), '%Y-%m-%d %H:%M:%S') > one_month_ago]
            LinhVucTD = [td['LinhVucTD'] for td in listTD]
            LinhVucTD = list(set(LinhVucTD))
            ViTriTD = [td['ViTriTD'] for td in listTD]
            ViTriTD = list(set(ViTriTD))
            NoiTD = [td['NoiTD'] for td in listTD]
            NoiTD = list(set(NoiTD))
            YeuCauCongViec = [td['YeuCauCongViec'] for td in listTD]
            YeuCauCongViec = list(set(YeuCauCongViec))
            DiaDiem = [
            "An Giang","Bà Rịa - Vũng Tàu","Bắc Giang","Bắc Kạn","Bạc Liêu","Bắc Ninh","Bến Tre","Bình Định","Bình Dương","Bình Phước","Bình Thuận","Cà Mau","Cần Thơ","Cao Bằng","Đà Nẵng", "Đắk Lắk","Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",  "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum" "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình","Thái Nguyên","Thanh Hóa","Thừa Thiên Huế","Tiền Giang","Thành phố Hồ Chí Minh","Trà Vinh","Tuyên Quang","Vĩnh Long","Vĩnh Phúc","Yên Bái"
            ]
            return template.TemplateResponse("index.html", {"request": request, 'listTD': listTD, 'userID' : userID, 'LinhVucTD': LinhVucTD, 'DiaDiem': DiaDiem, 'ViTriTD': ViTriTD, 'NoiTD': NoiTD, 'userType': "user", 'YeuCauCongVIec': YeuCauCongViec})
    def TongQuan(self, request, userID: str):
        listTD = tdController.GetAllTDs()
        listUser = user_controller.GetAllUser()
        listTT = tt_Controller.GetAllTT()
        listTDTT = tdController.GetTDTuongTac()
        percentage = user_controller.GetPhanTramSoVoiThangTruoc()
        return template.TemplateResponse("tongquan.html", {"request": request, 'userID': userID, 'listTD': listTD, 'listUser': listUser, 'listTT': listTT, 'listTDTT': listTDTT, 'percentage': percentage})
    def danhsachtk(self, request, userID: str):
        dstk = user_controller.GetAllUser()
        return template.TemplateResponse("danhsachtk.html", {"request": request, 'dstk': dstk, 'userID': userID})
    def danhsachQuanTam(self, request, IDTD: str):
        dstk = tdController.GetListUserTuongTacByIDTD(IDTD) 
        return template.TemplateResponse("danhsachQuanTam.html", {"request": request, 'dstk': dstk, 'IDTD': IDTD})
    def formChiTiet(self, request, IDTD: str, userID: str):
        user = user_controller.GetUserByGmail(userID)
        if user is None:
            user = ""
        return template.TemplateResponse("formchitiet.html", {"request": request, 'IDTD': IDTD, 'user': user})
    def formTimKiem(self, request, Text: str = None, LinhVucTD: str = None, DiaDiem: str = None, LuongTD: str = None, userID: str = None):
        if(LinhVucTD != None and DiaDiem != None and Text != None and LuongTD != None):
            listTD_Search = tdController.TimKiemTD(Text, LinhVucTD, DiaDiem, LuongTD)
            listTD_Search = sorted(listTD_Search, key=lambda x: datetime.strptime(str(x['NgayTD']), '%Y-%m-%d %H:%M:%S'), reverse=True)
            one_month_ago = datetime.now() - relativedelta(months=1)
            listTD_Search = [td for td in listTD_Search if datetime.strptime(str(td['NgayTD']), '%Y-%m-%d %H:%M:%S') > one_month_ago]
            LinhVucTD = None
            ViTriTD = None
            NoiTD = None
            YeuCauCongViec = None
            DiaDiem = [
            "An Giang","Bà Rịa - Vũng Tàu","Bắc Giang","Bắc Kạn","Bạc Liêu","Bắc Ninh","Bến Tre","Bình Định","Bình Dương","Bình Phước","Bình Thuận","Cà Mau","Cần Thơ","Cao Bằng","Đà Nẵng", "Đắk Lắk","Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",  "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum" "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình","Thái Nguyên","Thanh Hóa","Thừa Thiên Huế","Tiền Giang","Thành phố Hồ Chí Minh","Trà Vinh","Tuyên Quang","Vĩnh Long","Vĩnh Phúc","Yên Bái"
            ]
            listTD = tdController.GetAllTDs()
            listTD = [td for td in listTD if datetime.strptime(str(td['NgayTD']), '%Y-%m-%d %H:%M:%S') > one_month_ago]
            LinhVucTD = [td['LinhVucTD'] for td in listTD]
            LinhVucTD = list(set(LinhVucTD))
            ViTriTD = [td['ViTriTD'] for td in listTD]
            ViTriTD = list(set(ViTriTD))
            NoiTD = [td['NoiTD'] for td in listTD]
            NoiTD = list(set(NoiTD))
            YeuCauCongViec = [td['YeuCauCongViec'] for td in listTD]
            YeuCauCongViec = list(set(YeuCauCongViec))
            user = user_controller.GetUserByGmail(userID)
            if user is None:
                user = ""
            return template.TemplateResponse("formTimKiem.html", {"request": request, 'listTD': listTD_Search, 'LinhVucTD': LinhVucTD, 'DiaDiem': DiaDiem, 'ViTriTD': ViTriTD, 'NoiTD': NoiTD, 'YeuCauCongViec': YeuCauCongViec, 'user': user})
        else:
            listTD = tdController.GetAllTDs()
            one_month_ago = datetime.now() - relativedelta(months=1)
            listTD = [td for td in listTD if datetime.strptime(str(td['NgayTD']), '%Y-%m-%d %H:%M:%S') > one_month_ago]
            lvtd = [td['LinhVucTD'] for td in listTD]
            lvtd = list(set(lvtd))
            vttd = [td['ViTriTD'] for td in listTD]
            vttd = list(set(vttd))
            ntd = [td['NoiTD'] for td in listTD]
            ntd = list(set(ntd))
            tccv = [td['YeuCauCongViec'] for td in listTD]
            tccv = list(set(tccv))
            DiaDiem = [
            "An Giang","Bà Rịa - Vũng Tàu","Bắc Giang","Bắc Kạn","Bạc Liêu","Bắc Ninh","Bến Tre","Bình Định","Bình Dương","Bình Phước","Bình Thuận","Cà Mau","Cần Thơ","Cao Bằng","Đà Nẵng", "Đắk Lắk","Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",  "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum" "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình","Thái Nguyên","Thanh Hóa","Thừa Thiên Huế","Tiền Giang","Thành phố Hồ Chí Minh","Trà Vinh","Tuyên Quang","Vĩnh Long","Vĩnh Phúc","Yên Bái"
            ]
            user = user_controller.GetUserByGmail(userID)
            if user is None:
                user = ""
            return template.TemplateResponse("formTimKiem.html", {"request": request, 'listTD': None, 'LinhVucTD': lvtd, 'DiaDiem': DiaDiem, 'ViTriTD': vttd, 'NoiTD': ntd, 'YeuCauCongViec': tccv, 'user':user})