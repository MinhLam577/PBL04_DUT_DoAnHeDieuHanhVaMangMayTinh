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
    def __init__(self, driver, type="fanpage", nameOrID = 103274306376166, numberPost = 100, txt = None, timeout = 60):
        threading.Thread.__init__(self)
        self.driver = driver
        self.type = type #Lọc theo fanpage hoặc group
        self.nameOrId = nameOrID #ID hoặc tên của fanpage hoặc group
        self.numberPost = numberPost #Số lượng bài viết cần lấy trên mỗi fanpage hoặc group
        self.txt = txt #Từ khóa để tìm kiếm bài viết
        self.timeout = timeout #Thời gian kết thức tìm kiếm
    #Bắt đầu tìm kiếm ID của group hoặc fanpage
    def startLocIDGroupOrFanpage(self):
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
    #Bắt đầu lấy nội dung bài viết 
    def startGetContentPostBySelenium(self):
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
                try:
                    print("ID bài viết đã crawl:", ID)
                    self.driver.get("http://mbasic.facebook.com/"+ID)
                    postContent = getContentFromPostID(self.driver, ID)
                    if(postContent != None):
                        Text = postContent['ContentPost']
                        TimePost = postContent["TimePost"]
                        IDPost = postContent["IDPost"]
                        LinkPost = "https://www.facebook.com/"+IDPost
                        LinkImg = postContent["LinkImg"]
                        if(Text not in listAllContentPost and ID not in listAllIDPOST):
                            for tuKhoa in listTuKhoaViecLam:
                                if(tuKhoa in Text and one_week_ago <= TimePost <= now):
                                    print("Bai viet", i + 1, "\n\n","postID", IDPost, "Text",Text, "\nTime", TimePost, "\npostLink",LinkPost, "\npostImages",LinkImg, "\n\n")
                                    post = Post(IDPost=IDPost, TimePost=TimePost, ContentPost=Text, LinkPost=LinkPost, LinkImg=LinkImg)
                                    if(LinkImg != None):
                                        download_image(self.driver, LinkImg, IDPost)
                                    postController.AddPost(post)
                                    break
                except Exception as e:
                    print(f"Crawl bài viết có ID = {ID} của {self.type} thất bại, lỗi: " + getattr(e, 'message', repr(e)))
        elif(self.type == "group"):
            getPostsIDGroup(self.driver, FanpageOrGroupID, self.numberPost)
            listPostGroupID = readDataFileITxtID(filePostGroupID)
            for i, ID in enumerate(listPostGroupID):
                try:
                    self.driver.get("https://mbasic.facebook.com/"+ID)
                    postContent = getContentFromPostID(self.driver, ID)
                    if(postContent != None):
                        Text = postContent['ContentPost']
                        TimePost = postContent["TimePost"]
                        IDPost = postContent["IDPost"]
                        LinkPost = "https://www.facebook.com/"+IDPost
                        if postContent["LinkImg"] != None:
                            LinkImg = postContent["LinkImg"]
                        else:
                            LinkImg = None
                        if(Text not in listAllContentPost and ID not in listAllIDPOST):
                            for tuKhoa in listTuKhoaViecLam:
                                if(tuKhoa in Text and one_week_ago <= TimePost <= now):
                                    print("Bai viet",i + 1, "\n\n","postID", IDPost, "Text",Text, "\nTime", TimePost,
                                            "\npostLink",LinkPost, "\npostImages",LinkImg, "\n\n")
                                    post = Post(IDPost=IDPost, TimePost=TimePost, ContentPost=Text, LinkPost=LinkPost, LinkImg=LinkImg)
                                    if(LinkImg != None):
                                        download_image(self.driver, LinkImg, IDPost)
                                    postController.AddPost(post)
                                    break
                except Exception as e:
                    print(f"Crawl bài viết có ID = {ID} của {self.type} thất bại, lỗi: " + getattr(e, 'message', repr(e)))
    def closeDriverProfile(self):
        self.driver.close()
    def run(self):
        if(self.txt != None):
            self.startLocIDGroupOrFanpage()
        elif(self.txt == None):
            self.startGetContentPostBySelenium()             
def LocIDFanpageAndGroupPost(*,driver1, driver2, cookie1, cookie2, type1 = 'fanpage', type2 = 'group', txt, timeout = 60):
    try:
        driver1 = initDriverProfile("--headless=new")
        driver2 = initDriverProfile("--headless=new")
        loginFacebookByCookie(driver1, cookie1)
        loginFacebookByCookie(driver2, cookie2)
        thread1 = Threading(driver1, cookie=cookie1, type=type1, txt=txt, timeout=timeout)
        thread2 = Threading(driver2, cookie=cookie2, type=type2, txt=txt, timeout=timeout)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except Exception:
        traceback.print_exc()
    finally:
        thread1.closeDriverProfile()
        thread2.closeDriverProfile()
def getContentPostFanpageOrGroupBySelenium(*,driver, type = 'fanpage', NameOrID, numberPost = 100):
    try:
        thread = Threading(driver, type=type, numberPost=numberPost, nameOrID=NameOrID)
        thread.start()
        thread.join()
    except Exception:
        traceback.print_exc()
def startGetContentPostBySelenium(driver, type: str = "fanpage", NameOrID: str = None, numberPost: int = 10):
    try:
        getContentPostFanpageOrGroupBySelenium(driver=driver, type=type, numberPost=numberPost, NameOrID=NameOrID)
        print(f"Đã lấy xong bài viết của {type} có", "NameOrID", NameOrID)
        path = os.path.dirname(os.path.abspath(__file__)) + "/"
        with open(path + filePostFanpageID, 'w') as file:
            pass
        with open(path + filePostGroupID, 'w') as file:
            pass
        postController.DeleteDuplicatePost()
    except Exception:
        traceback.print_exc()
driver = initDriverProfile()
cookie = getCookieFromFile("cookies.txt")
loginFacebookByCookie(driver, cookie)

Check_type = False
while not Check_type:
    type = input("Nhập vào 0 nếu muốn crawl bài viết từ fanpage, 1 nếu muốn crawl bài viết từ group: ")
    Check_type = bool(re.match('^[0-1]$', type))
    if not Check_type:
        print("Vui lòng nhập 0 hoặc 1")
if(type == "0"):
    NameOrID = input("Nhập vào ID hoặc tên của fanpage: ")
    Check_type = False
    Count = None
    while not Check_type:
        Count = input("Nhập vào số lượng bài viết cần crawl: ")
        Check_type = bool(re.match('^\d+$', Count))
        if not Check_type:
            print("Số lượng bài viết phải là số nguyên")
        else:
            if(int(Count) <= 0):
                print("Số lượng bài viết phải lớn hơn 0")
    startGetContentPostBySelenium(driver, 'fanpage', NameOrID, int(Count))
elif type == "1":
    NameOrID = input("Nhập vào ID hoặc tên của group: ")
    Check_cnt = False
    Count = None
    while not Check_cnt:
        Count = input("Nhập vào số lượng bài viết cần crawl: ")
        Check_cnt = bool(re.match('^\d+$', Count))
        if not Check_cnt:
            print("Số lượng bài viết phải là số nguyên")
        else:
            if(int(Count) <= 0):
                print("Số lượng bài viết phải lớn hơn 0")
    startGetContentPostBySelenium(driver, 'group', NameOrID, int(Count))