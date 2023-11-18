from facebook_scraper import get_posts, set_cookies, exceptions
from seleniumCrawl import *
import os
import traceback
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
        listpost = []
        for i in range(numberPost):
            try:
                post = next(gen)
                if(post != None):
                    postID = post["post_id"]
                    Text = post["text"]  # Toàn bộ chữ có trong bài viết
                    time = post["time"]  # Thời gian đăng bài
                    userID = post["user_id"]  # ID người đăng bài
                    userName = post["username"]  # Tên người đăng bài
                    postLink = "https://www.facebook.com/"+postID
                    postImage = post["image"]
                    postImages = post["images"]  # Ảnh đại diện bài viết
                listpost.append({'IDPost':postID, 'ContentPost':Text, 'TimePost':time, 'IDUserSend':userID, 'NameUserSend':userName, 'LinkPost':postLink, 'LinkImg':postImages})
                print("Bai viet",i + 1, "\n\n","postID", postID, "Text",Text, "\nTime", time, "\nuserID",userID,"\nuserName",userName, "\npostLink",postLink, "\npostImage",postImage, "\npostImages",postImages, "\n\n")
                return listpost
            except exceptions.TemporarilyBanned:
                print("Temporarily banned")
                break
            except Exception:
                traceback.print_exc()
        return post
    except Exception:
        traceback.print_exc()
