from facebook_scraper import get_posts, set_cookies, exceptions
from seleniumCrawl import *
import os
import traceback
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from App.Controllers.PostController import *
#Lưu ý phương pháp này trước khi sử dụng phải reset lại cookies
def setCookie(filename):
    set_cookies(os.path.dirname(os.path.abspath(__file__)) + "/" + filename)

def GetContentPost(type="fanpage", nameOrID = 103274306376166, numberPost = 100):
    """
    Hàm này để lấy nội dung từ fanpage, group hoặc post\n
    type: "fanpage" or "group" or "post"
    nameOrID: Tên hoặc ID của fanpage, group hoặc post, có thể truyền vào chuỗi hoặc số nguyên
    numberPost: Số lượng bài viết muốn lấy mặc định là 100 đối với type = post thì numberPost sẽ tự chuyển về 1
    """
    try:
        setCookie("cookies.txt")
        options={
                "allow_extra_requests": False, #Allow extra requests để lấy ảnh có chất lượng tốt ko nên vì dễ gây ban
                "posts_per_page": 200, #bài viết trên 1 trang
        }
        if(type == "fanpage"):
            gen = get_posts(
                        account=nameOrID, #fanpage name hoặc fanpage ID
                        options=options
                    )
        elif(type == "group"):
            gen = get_posts(
                        group=nameOrID, #fanpage name hoặc fanpage ID
                        options=options
                    )
        elif(type == "post"):
            gen = get_posts(
                        post_urls=[str(nameOrID)], #fanpage name hoặc fanpage ID
                        options=options
                    )
            numberPost = 1
        postController = PostControllers()
        i = 0
        while i < numberPost:
            try:
                listTuKhoaViecLam = ["tuyển", "tuyển dụng", "vị trí", "chiêu mộ", "cần", "gấp", "lương", "năm kinh nghiệm", "năm kn", "phúc lợi", "cần tìm", "benefit", "job", "tìm kiếm", "offer", "offer up to", "đãi ngộ", "chế độ đãi ngộ", "ứng viên", "cơ hội", "YÊU CẦU", "quyền lợi", "CV", "mô tả công việc", "nhân sự", "up to"]
                listAllContentPost = postController.GetAllContentPost()
                listAllIDPOST = postController.GetAllIDPost()
                post = next(gen)
                if(post != None):
                    if post["text"] not in listAllContentPost and post["post_id"] not in listAllIDPOST:
                        IDPost = post["post_id"]
                        ContentPost = post["text"] # Toàn bộ chữ có trong bài viết
                        TimePost = post["time"]  # Thời gian đăng bài
                        IDUserSend = post["user_id"]  # ID người đăng bài
                        NameUserSend = post["username"]  # Tên người đăng bài
                        LinkPost = "https://www.facebook.com/"+IDPost
                        LinkImg = post["images"]  # Ảnh đại diện bài viết
                        for tuKhoa in listTuKhoaViecLam:
                            if(tuKhoa in ContentPost):
                                print("Bai viet",i + 1, "\n\n","postID", IDPost, "Text",ContentPost, "\nTime", TimePost,
                                    "\nuserID",IDUserSend,"\nuserName",NameUserSend, "\npostLink",LinkPost, 
                                    "\npostImages",LinkImg, "\n\n")
                                post = Post(IDPost=IDPost, TimePost=TimePost, ContentPost=ContentPost, IDUserSend=IDUserSend,
                                            NameUserSend=NameUserSend, LinkPost=LinkPost, LinkImg=LinkImg)
                                postController.AddPost(post)
                                i += 1
                                break
                sleep(5)
            except exceptions.TemporarilyBanned:
                print("Temporarily banned")
                break
            except Exception:
                pass
    except Exception:
        traceback.print_exc()
