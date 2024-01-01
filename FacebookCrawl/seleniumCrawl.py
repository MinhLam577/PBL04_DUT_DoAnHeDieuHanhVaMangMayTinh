import os
from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import re
import traceback
import sys
from datetime import datetime, timedelta
import datetime as dt
import dateutil.parser
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from App.Controllers.PostController import *
fileGroupID = 'ID_Group.txt'
fileFanpageID = 'ID_Fanpage.txt'
filePostFanpageID = 'post_ID_Fanpage.txt'
filePostGroupID = 'post_ID_Group.txt'
fileGroupIDJoin = "ID_Group_Join.txt"
postController = PostControllers()
# khởi tạo 1 chrome profile với tham số headless(ẩn chrome) tùy chọn
def initDriverProfile(headlessOption='--disable-headless'): 
    # Đường dẫn đến thư mục chứa file python hiện tại
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Đường dẫn đến file chromedriver.exe
    CHROMEDRIVER_PATH = current_directory + "\chromedriver.exe";
    Service = webdriver.chrome.service.Service(CHROMEDRIVER_PATH)
    Options = webdriver.ChromeOptions()
    Options.add_argument('--no-sandbox')
    Options.add_argument("--disable-blink-features=AutomationControllered")
    Options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    Options.add_experimental_option("prefs", prefs)
    Options.add_argument("--disable-dev-shm-usage")
    Options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Ẩn chrome --headless=new không ẩn --disable-headless
    Options.add_argument(headlessOption) 
    # không hiển thị thông báo đăng nhập chrome
    Options.add_argument("--disable-infobars")
    # Hiển thị lớn nhất trình duyệt
    Options.add_argument("--start-minimized")
    # không hiển thị thông báo extensions
    Options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(service=Service, options=Options)
    return driver

# Đăng nhập bằng cookie
def loginFacebookByCookie(driver, cookie):
    try:
        cookie = getCookieByRawCookie(cookie)
        if (cookie != None):
            #Định dạng cookie facebook 
            #cookie = "c_user=XXXXXX;domain=.facebook.com;expires=XXXXXX;xs=XXXXXX;domain=.facebook.com;expires=XXXXXX;"
            script='javascript:void(function(){function setCookie(t) {for(i of t.split("; ")){var d = new Date();d.setTime(d.getTime() + (7*24*60*60*1000));var expires = ";domain=.facebook.com;expires="+ d.toUTCString();var cookie = i + expires + ";";document.cookie=cookie;}} location.href = "https://mbasic.facebook.com";setCookie("' + cookie +'"); })();'
            driver.execute_script(script)
    except Exception:
        traceback.print_exc()

#Lấy cookie từ raw cookie trên facebook network
def getCookieByRawCookie(cookie):
    try:
        new_cookie = ["c_user=", "xs="]
        cookie_arr = cookie.split(";")
        for i in cookie_arr:
            if i.__contains__('c_user='):
                new_cookie[0] = new_cookie[0] + (i.strip() + ";").split("c_user=")[1]
            if i.__contains__('xs='):
                new_cookie[1] = new_cookie[1] + (i.strip() + ";").split("xs=")[1]
                if (len(new_cookie[1].split("|"))):
                    new_cookie[1] = new_cookie[1].split("|")[0]
                if (";" not in new_cookie[1]):
                    new_cookie[1] = new_cookie[1] + ";"
        conv = new_cookie[0] + " " + new_cookie[1]
        if (conv.split(" ")[0] == "c_user="):
            return
        else:
            return conv
    except Exception:
        traceback.print_exc()
        
#Lấy cookie từ file
def getCookieFromFile(filename):
    try:
        path = os.path.dirname(os.path.abspath(__file__)) + "/" + filename
        if(os.path.isfile(path) == False):
            raise Exception("File not found")
        with open(path, mode='r') as f:
            c_user = ""
            xs = ""
            for i, line in enumerate(f):
                if line.__contains__('c_user') or line.__contains__('xs'):
                    if(line.__contains__('c_user') and c_user == ""):
                        c_user = line[line.find('c_user'): -1].strip().replace('\t', '=')
                    elif(line.__contains__('xs') and xs == ""):
                        xs = line[line.find('xs'): -1].strip().replace('\t', '=')
            cookie = c_user + '; ' + xs + ';'
            if(re.findall(r'c_user=(.*?);', cookie)[0] == ''):
                raise Exception("Cookie not found")
            return cookie
    except Exception:
        traceback.print_exc()
        return None

#Đọc dữ liệu từ file txt
def readDataFileITxtID(fileName):
    try:
        path = os.path.dirname(os.path.abspath(__file__)) + "/" + fileName
        if (os.path.isfile(path) == False):
            with open(path, 'a', encoding='utf-8') as f:
                pass
            return []
        else:
            with open(path, 'r', encoding='utf-8') as f:
                data = [line.split(";") for line in f]
                data = [item for sublist in data for item in sublist]
            return data[0:-1]
    except Exception:
         traceback.print_exc()

#Ghi dữ liệu vào file txt
def writeFileTxtID(fileName, content):
    try:
        path = os.path.dirname(os.path.abspath(__file__)) + "/" + fileName
        with open(path, 'a') as f1:
            f1.write(content + ";")
    except Exception:
        traceback.print_exc()
        
#Kéo đến cuối trang trong selenium
def scrollToEndOfPage(driver, timeout = 60):
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        start_time = time.time()
        while (True):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if (new_height == last_height or time.time() - start_time > float(timeout)):
                break
            last_height = new_height
    except Exception:
        traceback.print_exc()

#Tìm kiếm ID bài viết trên fanpage
def get_FangpageID_By_Search(driver, txt, timeout = 15):
    try:
        driver.get("https://www.facebook.com/search/pages?q=" + txt)
        sleep(2)
        scrollToEndOfPage(driver, timeout)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listFanpage = soup.find_all('div', attrs={'data-visualcompletion': 'ignore-dynamic'})
        listFanpageName = [i.find('a', attrs={'aria-hidden':'true', 'role':'presentation', 'href' : lambda x: x and re.match("https:\/\/www\.facebook\.com\/((profile\.php\?id=\d+)|([a-zA-Z0-9\.]){5,})", x)}) for i in listFanpage]
        for i in range(len(listFanpageName)):
            if(listFanpageName[i] != None):
                if(listFanpageName[i]['href'].__contains__('profile.php')):
                    listFanpageName[i] = listFanpageName[i]['href'].split('/')[-1].split('?id=')[-1]
                else:
                    listFanpageName[i] = listFanpageName[i]['href'].split('/')[-1]
        listFanpageName = [i for i in listFanpageName if i != None]
        return listFanpageName
    except NoSuchElementException:
        raise NoSuchElementException

#Tìm kiếm ID bài viết của Group 
def get_GroupPublicID_By_Search(driver, txt, timeout = 60):
    try:
        driver.get("https://www.facebook.com/groups/search/groups/?q=" + txt + "&filters=eyJwdWJsaWNfZ3JvdXBzOjAiOiJ7XCJuYW1lXCI6XCJwdWJsaWNfZ3JvdXBzXCIsXCJhcmdzXCI6XCJcIn0ifQ%3D%3D")
        sleep(2)
        scrollToEndOfPage(driver, timeout)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listGroup = soup.find('div', attrs={'aria-label':'Kết quả tìm kiếm'}).find_all('div', attrs={'data-visualcompletion': 'ignore-dynamic', 'style': lambda x: x and 'padding-left:' in x})
        listGroupName = [i.find('a', attrs={'aria-hidden':'true', 'role':'presentation', 'href' : lambda x: x and re.match("https:\/\/www\.facebook\.com\/groups\/(([a-zA-Z0-9\.]){5,}|\d+)", x)}) for i in listGroup]
        listGroupIDOrName = [i['href'][:-1].split('/')[-1] for i in listGroupName if i != None]
        return listGroupIDOrName
    except NoSuchElementException:
        raise NoSuchElementException

#Tìm kiếm ID bài viết của các đã join
def get_JoinedGroupID_By_Search(driver, txt, timeout = 60):
    try:
        driver.get("https://www.facebook.com/groups/search/groups/?q=" + txt + "&filters=eyJteV9ncm91cHM6MCI6IntcIm5hbWVcIjpcIm15X2dyb3Vwc1wiLFwiYXJnc1wiOlwiXCJ9In0%3D")
        sleep(2)
        scrollToEndOfPage(driver, timeout)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listGroup = soup.find('div', attrs={'aria-label':'Kết quả tìm kiếm'}).find_all('div', attrs={'data-visualcompletion': 'ignore-dynamic', 'style': lambda x: x and 'padding-left:' in x})
        listGroupName = [i.find('a', attrs={'aria-hidden':'true', 'role':'presentation', 'href' : lambda x: x and re.match("https:\/\/www\.facebook\.com\/groups\/(([a-zA-Z0-9\.]){5,}|\d+)", x)}) for i in listGroup]
        listGroupIDOrName = [i['href'][:-1].split('/')[-1] for i in listGroupName if i != None]
        return listGroupIDOrName
    except NoSuchElementException:
        raise NoSuchElementException

#Lấy post ID của bài viết trong group
def getPostsIDGroup(driver, idGroup, numberPost=10):
    try:
        driver.get('https://mbasic.facebook.com/groups/' + str(idGroup))
        sleep(2)
        listAllIDPOST = postController.GetAllIDPost()
        sumLinks = readDataFileITxtID(filePostGroupID)
        while (len(sumLinks) < numberPost):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                likeBtn = driver.find_elements(By.XPATH, '//*[contains(@id, "like_")]')
                if len(likeBtn):
                    for id in likeBtn:
                        idPost = id.get_attribute('id').replace("like_", "")
                        if (idPost not in sumLinks and len(sumLinks) < numberPost and idPost not in listAllIDPOST):
                            sumLinks.append(idPost)
                            print("Đã lọc được bài viết có ID:", idPost)
                            writeFileTxtID(filePostGroupID, idPost)
                nextBtn = driver.find_elements(By.XPATH, '//a[contains(@href, "?bacr")]')
                if (len(nextBtn)):
                    nextBtn[0].click()
                    sleep(2)
                else:
                    break
            except WebDriverException:
                traceback.print_exc()
                break
            except Exception:
                traceback.print_exc()
    except NoSuchElementException:
        raise NoSuchElementException
    except AttributeError:
        raise AttributeError
    except Exception:
        traceback.print_exc()

#Lấy Post ID của bài viết trong Fanpage
def getPostIDFanpage(driver, idFanpage, numberpost=10):
    try:
        driver.get("https://mbasic.facebook.com/" + str(idFanpage));
        sleep(2)
        listAllIDPOST = postController.GetAllIDPost()
        # địa chỉ URL hiện tại
        current_url = driver.current_url
        # lấy tên người dùng
        nameUser = current_url.split("/")[-1]
        timeline = driver.find_element(By.XPATH, "//a[starts-with(@href, '/" + nameUser + "?v=timeline')]")
        timeline.click()
        sleep(2)
        sumLinks = readDataFileITxtID(filePostFanpageID)
        while (len(sumLinks) < numberpost):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                likeBtn = driver.find_elements(By.XPATH, '//*[contains(@id, "like_")]')
                if len(likeBtn):
                    for id in likeBtn:
                        idPost = id.get_attribute('id').replace("like_", "")
                        if (idPost not in sumLinks and len(sumLinks) < numberpost and idPost not in listAllIDPOST):
                            sumLinks.append(idPost)
                            print("Đã lọc được bài viết có ID:", idPost)
                            writeFileTxtID(filePostFanpageID, idPost)
                nextBtn = driver.find_elements(By.XPATH, '//a[contains(@href, "?cursor=")]')
                if (len(nextBtn)):
                    nextBtn[0].click()
                    sleep(2)
                else:
                    break
            except WebDriverException:
                traceback.print_exc()
    except NoSuchElementException:
        raise NoSuchElementException
    except AttributeError:
        raise AttributeError
    except Exception:
        traceback.print_exc()

def parse_date(date_string):
    try:
        parsed_date = datetime.strptime(date_string, "%d tháng %m lúc %H:%M")
        # Nếu không có năm, giả định năm hiện tại
        if parsed_date.year == 1900:
            parsed_date = parsed_date.replace(year=datetime.now().year)
        return parsed_date
    except ValueError:
        try:
            # Thử định dạng "ngày tháng năm, năm lúc giờ:phút"
            return datetime.strptime(date_string, "%d tháng %m, %Y lúc %H:%M")
        except ValueError:
            try:
                # Thử định dạng "Hôm qua lúc giờ:phút"
                if "Hôm qua" in date_string:
                    yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                    time = datetime.strptime(date_string.split(" lúc ")[1], "%H:%M").time()
                    return datetime.combine(yesterday, time)
                else: 
                    raise ValueError(date_string)
            except ValueError:
                try:
                    # Thử định dạng "x giờ"
                    if "giờ" in date_string:
                        hours_ago = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=int(date_string.split(" ")[0]))
                        return hours_ago
                    else:
                        raise ValueError(date_string)
                except ValueError:
                    try:
                        # Thử định dạng "x phút"
                        if "phút" in date_string:
                            minutes_ago = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(minutes=int(date_string.split(" ")[0]))
                            return minutes_ago
                        else:
                            raise ValueError(date_string)
                    except ValueError:
                        try:
                            # Thử định dạng "x giây"
                            if "giây" in date_string:
                                seconds_ago = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=int(date_string.split(" ")[0]))
                                return seconds_ago
                            else:
                                raise ValueError(date_string)
                        except ValueError:
                            # Nếu tất cả các định dạng trên đều không khớp, sử dụng dateutil.parser
                            return dateutil.parser.parse(date_string)
#Lấy nội dung bài viết từ ID post
def getContentFromPostID(driver, postID):
    try:
        driver.get("http://mbasic.facebook.com/"+postID)
        sleep(2)
        scrollToEndOfPage(driver)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        contentBox = soup.find('div', id='m_story_permalink_view')
        content = contentBox.find('div', attrs={'data-ft': '{\"tn\":\"*s\"}'})
        imgGroup = contentBox.find('div', attrs={'data-ft': '{\"tn\":\"H\"}'})
        footer = contentBox.find('footer', attrs={'data-ft': '{\"tn\":\"*W\"}'})
        obj = {'IDPost': postID}
        if (content != None):
            obj['ContentPost'] = content.get_text()
        if (footer != None):
            timepost = footer.find('abbr').get_text()
            timepost = parse_date(timepost)
            obj['TimePost'] = timepost
        if(imgGroup != None):
            list_a = imgGroup.find_all('a', attrs={'href': lambda x: x and ("photo" in x)})
            if(list_a != None and len(list_a) > 0):
                list_href = ["http://www.facebook.com"+i['href'] for i in list_a]
                LinkImg = list_href[0]
                obj['LinkImg'] = LinkImg
            else:
                obj['LinkImg'] = None
        else:
            obj['LinkImg'] = None
        obj['LinkPost'] = "http://www.facebook.com/" + postID
        return obj
    except AttributeError:
        raise AttributeError
    except Exception:
        traceback.print_exc()
#Tải ảnh
def download_image(driver, url, IDpost):
    try:
        driver.get(url)
        sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        image_src = soup.find('img', {'data-visualcompletion': 'media-vc-image'})
        if image_src is None:
            return
        image_src = image_src['src']
        # Đường dẫn đến thư mục chứa file python hiện tại
        current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #Đường dẫn đến folder ảnh
        folder_path = os.path.join(current_directory,"App\\View\\static\\images\\TDImages")
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        # Đường dẫn đến ảnh
        filename = os.path.join(folder_path, f"{IDpost}.jpg")
        response = requests.get(image_src, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print("download file err, error: ", getattr(e, 'message', repr(e)))

