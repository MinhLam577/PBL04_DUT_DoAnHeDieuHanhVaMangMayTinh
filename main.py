from FacebookCrawl.scraperCrawl import *
from FacebookCrawl.seleniumCrawl import *
from datetime import datetime
from router.indexRouter import *
import uvicorn
import traceback
import threading
class Threading(threading.Thread):
    def __init__(self, driver, cookie, type="fanpage", nameOrID = 103274306376166, numberPost = 100, txt = None, timeout = 60):
        threading.Thread.__init__(self)
        self.driver = driver
        self.cookie = cookie
        self.type = type
        self.nameOrId = nameOrID
        self.numberPost = numberPost
        self.txt = txt
        self.timeout = timeout
    def startLocIDBaiViet(self):
        loginFacebookByCookie(self.driver, getCookieByRawCookie(self.cookie))
        if(self.type == "fanpage"):
            dataFileID1 = readDataFileITxtID(fileFanpageID)
            dataID1 = get_FangpageID_By_Search(self.driver, self.txt, self.timeout)
            for ID in dataID1:
                if(ID not in dataFileID1):
                    dataFileID1.append(ID)
                    writeFileTxtID(fileFanpageID, ID)
        elif(self.type == "group"):
            dataFileID2 = readDataFileITxtID(fileGroupID)
            dataID2 = get_GroupPublicID_By_Search(self.driver, self.txt, self.timeout)
            for ID in dataID2:
                if(ID not in dataFileID2):
                    dataFileID2.append(ID)
                    writeFileTxtID(fileGroupID, ID)
    def startGetContentPostBySelenium(self):
        listTuKhoaViecLam = ["tuyển", "tuyển dụng", "vị trí", "chiêu mộ", "cần", "gấp", "lương", "năm kinh nghiệm", "năm kn", "phúc lợi", "cần tìm", "benefit", "job", "tìm kiếm", "offer", "offer up to", "đãi ngộ", "chế độ đãi ngộ", "ứng viên", "cơ hội", "YÊU CẦU", "quyền lợi", "CV", "mô tả công việc", "nhân sự", "up to"]
        if(self.type == "fanpage"):
            listPostFanpageID = readDataFileITxtID(filePostFanpageID)
            for ID in listPostFanpageID:
                self.driver.get("https://mbasic.facebook.com/"+ID)
                postContent = getContentFromPostID(self.driver, ID)
                Text = postContent['ContentPost']
                if(Text != ""):
                    for tuKhoa in listTuKhoaViecLam:
                        if(tuKhoa in Text):
                            print(postContent)
        elif(self.type == "group"):
            listPostGroupID = readDataFileITxtID(filePostGroupID)
            for ID in listPostGroupID:
                self.driver.get("https://mbasic.facebook.com/"+ID)
                postContent = getContentFromPostID(self.driver, ID)
                Text = postContent['ContentPost']
                if(Text != ""):
                    for tuKhoa in listTuKhoaViecLam:
                        if(tuKhoa in Text):
                            print(postContent)
    def closeDriverProfile(self):
        self.driver.close()
    def run(self):
        pass
                    
def LocIDFanpageAndGroupPost(*,driver1, driver2, cookie1, cookie2, type1 = 'fanpage', type2 = 'group', txt, timeout = 60):
    try:
        thread1 = Threading(driver1, cookie=cookie1, type=type1, txt=txt, timeout=timeout)
        thread2 = Threading(driver2, cookie=cookie2,type=type2, txt=txt, timeout=timeout)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except Exception:
        traceback.print_exc()
    finally:
        thread1.closeDriverProfile()
        thread2.closeDriverProfile()

def getContentPostFanpageOrGroupBySelenium(*,driver1, driver2, cookie1, cookie2, type1 = 'fanpage', type2 = 'group', numberPost = 100):
    try:
        thread1 = Threading(driver1, cookie=cookie1,type=type1, numberPost=numberPost)
        thread2 = Threading(driver2, cookie=cookie2,type=type2, numberPost=numberPost)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except Exception:
        traceback.print_exc()
    finally:
        thread1.closeDriverProfile()
        thread2.closeDriverProfile()
        
def getContentPostByScraper(*,type = 'fanpage', nameOrID, numberPost = 100):
    listTuKhoaViecLam = ["tuyển", "tuyển dụng", "vị trí", "chiêu mộ", "cần", "gấp", "lương", "năm kinh nghiệm", "năm kn", "phúc lợi", "cần tìm", "benefit", "job", "tìm kiếm", "offer", "offer up to", "đãi ngộ", "chế độ đãi ngộ", "ứng viên", "cơ hội", "YÊU CẦU", "quyền lợi", "CV", "mô tả công việc", "nhân sự", "up to"]
    listPost = GetContentPost(type, nameOrID, numberPost)
    for post in listPost:
        text = post['ContentPost']
        if(text != ""):
            for tuKhoa in listTuKhoaViecLam:
                if tuKhoa in text:
                    print(post)
                    break
if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    except Exception:
        traceback.print_exc()
