from scraperCrawl import *
from seleniumCrawl import *
import traceback
import threading
import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from App.Controllers.PostController import *
postController = PostControllers()
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
        loginFacebookByCookie(self.driver, getCookieByRawCookie(self.cookie))
        listTuKhoaViecLam = ["tuyển", "tuyển dụng", "vị trí", "chiêu mộ", "lương", "năm kinh nghiệm", "năm kn", "phúc lợi", "benefit", "job", "offer", "offer up to", "đãi ngộ", "chế độ đãi ngộ", "ứng viên", "cơ hội", "YÊU CẦU", "quyền lợi", "CV", "mô tả công việc", "nhân sự", "up to"]
        listAllContentPost = postController.GetAllContentPost()
        listAllIDPOST = postController.GetAllIDPost()
        FanpageOrGroupID = self.nameOrId
        # Lấy thời gian hiện tại
        now = dt.datetime.now().replace(microsecond=0)
        # Lấy thời gian cách hiện tại 1 tuần
        one_week_ago = now - dt.timedelta(weeks=1)
        if(self.type == "fanpage"):
            getPostIDFanpage(self.driver, FanpageOrGroupID, self.numberPost)
            listPostFanpageID = readDataFileITxtID(filePostFanpageID)
            for i, ID in enumerate(listPostFanpageID):
                self.driver.get("https://mbasic.facebook.com/"+ID)
                postContent = getContentFromPostID(self.driver, ID)
                if(postContent != None):
                    Text = postContent['ContentPost']
                    if(Text not in listAllContentPost and ID not in listAllIDPOST):
                        for tuKhoa in listTuKhoaViecLam:
                            if(tuKhoa in Text and one_week_ago <= TimePost <= now):
                                IDPost = postContent["post_id"]
                                ContentPost = postContent["text"] # Toàn bộ chữ có trong bài viết
                                TimePost = postContent["time"]  # Thời gian đăng bài
                                IDUserSend = postContent["user_id"]  # ID người đăng bài
                                NameUserSend = postContent["username"]  # Tên người đăng bài
                                LinkPost = "https://www.facebook.com/"+IDPost
                                LinkImg = postContent["images"]  # Ảnh đại diện bài viết
                                print("Bai viet", i + 1, "\n\n","postID", IDPost, "Text",ContentPost, "\nTime", TimePost,
                                        "\nuserID",IDUserSend,"\nuserName",NameUserSend, "\npostLink",LinkPost, 
                                        "\npostImages",LinkImg, "\n\n")
                                post = Post(IDPost=IDPost, TimePost=TimePost, ContentPost=ContentPost, IDUserSend=IDUserSend,
                                            NameUserSend=NameUserSend, LinkPost=LinkPost, LinkImg=LinkImg)
                                postController.AddPost(post)
                                break
        elif(self.type == "group"):
            getPostsIDGroup(self.driver, FanpageOrGroupID, self.numberPost)
            listPostGroupID = readDataFileITxtID(filePostGroupID)
            for i, ID in enumerate(listPostGroupID):
                self.driver.get("https://mbasic.facebook.com/"+ID)
                postContent = getContentFromPostID(self.driver, ID)
                if(postContent != None):
                    Text = postContent['ContentPost']
                    TimePost = postContent["TimePost"]
                    if(Text not in listAllContentPost and ID not in listAllIDPOST):
                        for tuKhoa in listTuKhoaViecLam:
                            if(tuKhoa in Text and one_week_ago <= TimePost <= now):
                                IDPost = postContent["post_id"]
                                ContentPost = postContent["text"] # Toàn bộ chữ có trong bài viết
                                TimePost = postContent["time"]  # Thời gian đăng bài
                                IDUserSend = postContent["user_id"]  # ID người đăng bài
                                NameUserSend = postContent["username"]  # Tên người đăng bài
                                LinkPost = "https://www.facebook.com/"+IDPost
                                LinkImg = postContent["images"]  # Ảnh đại diện bài viết
                                print("Bai viet",i + 1, "\n\n","postID", IDPost, "Text",ContentPost, "\nTime", TimePost,
                                        "\nuserID",IDUserSend,"\nuserName",NameUserSend, "\npostLink",LinkPost, 
                                        "\npostImages",LinkImg, "\n\n")
                                post = Post(IDPost=IDPost, TimePost=TimePost, ContentPost=ContentPost, IDUserSend=IDUserSend,
                                            NameUserSend=NameUserSend, LinkPost=LinkPost, LinkImg=LinkImg)
                                postController.AddPost(post)
                                break
    def closeDriverProfile(self):
        self.driver.close()
    def run(self):
        if(self.txt != None):
            self.startLocIDBaiViet()
        elif(self.txt == None):
            self.startGetContentPostBySelenium()             
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

def getContentPostFanpageOrGroupBySelenium(*,driver, cookie, type = 'fanpage', NameOrID, numberPost = 100):
    try:
        thread = Threading(driver, cookie=cookie, type=type, numberPost=numberPost, nameOrID=NameOrID)
        thread.start()
        thread.join()
    except Exception:
        traceback.print_exc()
    finally:
        thread.closeDriverProfile()
postController = PostControllers()
def getContentPostByScraper(*,type = 'fanpage', nameOrID, numberPost = 100):
    GetContentPost(type=type, nameOrID=nameOrID, numberPost=numberPost)
def startGetContentPostByScraper():
    try:
        listIDGroup = readDataFileITxtID(fileGroupID)
        driver1 = initDriverProfile()
        cookie = getCookieFromFile("cookies.txt")
        loginFacebookByCookie(driver1, cookie)
        for i, ID in enumerate(listIDGroup):
            getPostsIDGroup(driver1, ID, 10)
            lisPostIDGroup = readDataFileITxtID("post_ID_Group.txt")
            for PostID in lisPostIDGroup:
                getContentPostByScraper(type="post", nameOrID=PostID, numberPost=1)
                sleep(2)
            print("Đã lấy xong bài viết của group", i + 1, "ID", ID)
            postController.DeleteDuplicatePost()
            path = os.path.dirname(os.path.abspath(__file__)) + "/"
            with open(path + 'post_ID_Group.txt', 'w') as file:
                pass
    except Exception: 
        traceback.print_exc()
def startGetContentPostBySelenium():
    try:
        driver1 = initDriverProfile()
        cookie = getCookieFromFile("cookies.txt")
        listIDGroup = readDataFileITxtID(fileGroupID)
        for i, ID in enumerate(listIDGroup, 1):
            getContentPostFanpageOrGroupBySelenium(driver=driver1, cookie=cookie, type="group", numberPost=10, NameOrID=ID)
            print("Đã lấy xong bài viết của group", i, "ID", ID)
            postController.DeleteDuplicatePost()
    except Exception:
        traceback.print_exc()
startGetContentPostByScraper()