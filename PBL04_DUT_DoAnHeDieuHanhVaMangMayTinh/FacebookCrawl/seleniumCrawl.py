import os
from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
import re
import traceback

fileGroupID = 'ID_Group.txt'
fileFanpageID = 'ID_Fanpage.txt'
filePostFanpageID = 'post_ID_Fanpage.txt'
filePostGroupID = 'post_ID_Group.txt'
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
    # Ẩn chrome
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

#Lấy cookie từ raw cookie trên facebook profile
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

def writeFileTxtID(fileName, content):
    try:
        path = os.path.dirname(os.path.abspath(__file__)) + "/" + fileName
        with open(path, 'a') as f1:
            f1.write(content + ";")
    except Exception:
        traceback.print_exc()
        
def scrollToEndOfPage(driver, timeout = 60):
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        start_time = time.time()
        while (True):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if (new_height == last_height or time.time() - start_time > timeout):
                break
            last_height = new_height
    except Exception:
        traceback.print_exc()

def get_FangpageID_By_Search(driver, txt, timeout = 60):
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
    print(listFanpageName)
    return listFanpageName

def get_GroupPublicID_By_Search(driver, txt, timeout = 60):
    driver.get("https://www.facebook.com/groups/search/groups/?q=" + txt + "&filters=eyJwdWJsaWNfZ3JvdXBzOjAiOiJ7XCJuYW1lXCI6XCJwdWJsaWNfZ3JvdXBzXCIsXCJhcmdzXCI6XCJcIn0ifQ%3D%3D")
    sleep(2)
    scrollToEndOfPage(driver, timeout)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    listGroup = soup.find('div', attrs={'aria-label':'Kết quả tìm kiếm'}).find_all('div', attrs={'data-visualcompletion': 'ignore-dynamic', 'style': lambda x: x and 'padding-left:' in x})
    listGroupName = [i.find('a', attrs={'aria-hidden':'true', 'role':'presentation', 'href' : lambda x: x and re.match("https:\/\/www\.facebook\.com\/groups\/(([a-zA-Z0-9\.]){5,}|\d+)", x)}) for i in listGroup]
    listGroupIDOrName = [i['href'][:-1].split('/')[-1] for i in listGroupName if i != None]
    return listGroupIDOrName

def get_JoinedGroupID_By_Search(driver, txt, timeout = 60):
    driver.get("https://www.facebook.com/groups/search/groups/?q=" + txt + "&filters=eyJteV9ncm91cHM6MCI6IntcIm5hbWVcIjpcIm15X2dyb3Vwc1wiLFwiYXJnc1wiOlwiXCJ9In0%3D")
    sleep(2)
    scrollToEndOfPage(driver, timeout)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    listGroup = soup.find('div', attrs={'aria-label':'Kết quả tìm kiếm'}).find_all('div', attrs={'data-visualcompletion': 'ignore-dynamic', 'style': lambda x: x and 'padding-left:' in x})
    listGroupName = [i.find('a', attrs={'aria-hidden':'true', 'role':'presentation', 'href' : lambda x: x and re.match("https:\/\/www\.facebook\.com\/groups\/(([a-zA-Z0-9\.]){5,}|\d+)", x)}) for i in listGroup]
    listGroupIDOrName = [i['href'][:-1].split('/')[-1] for i in listGroupName if i != None]
    return listGroupIDOrName
#Lấy Posts From Fanpage
def getPostsFromFanpage(driverCrawPostID, driverCrawPostContent, idFanpage, numberpost=100):
    try:
        driverCrawPostID.driver.get("https://mbasic.facebook.com/" + str(idFanpage));
        sleep(2)
        # địa chỉ URL hiện tại
        current_url = driverCrawPostID.driver.current_url
        # lấy tên người dùng
        nameUser = current_url.split("/")[-1]
        timeline = driverCrawPostID.driver.find_element(By.XPATH, f"//a[starts-with(@href,'/{nameUser}?v=timeline)']")
        timeline.click()
        sleep(2)
        sumLinks = readDataFileITxtID(fileFanpageID)
        while (len(sumLinks) < numberpost):
            driverCrawPostID.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            likeBtn = driverCrawPostID.driver.find_elements(By.XPATH, '//*[contains(@id, "like_")]')
            if len(likeBtn):
                for id in likeBtn:
                    idPost = id.get_attribute('id').replace("like_", "")
                    if (idPost not in sumLinks and len(sumLinks) <= numberpost):
                        driverCrawPostContent.driver.get("https://mbasic.facebook.com/" + str(idPost))
                        print(idPost)
                        sumLinks.append(idPost)
                        print("Bài viêt:", len(sumLinks))
                        Content = getContentFromPostID(driverCrawPostContent.driver)
                        sleep(2)
                        print(Content)
                        writeFileTxtID(fileFanpageID, idPost)
            nextBtn = driverCrawPostID.driver.find_elements(By.XPATH, '//a[contains(@href, "?cursor=")]')
            if (len(nextBtn)):
                nextBtn[0].click()
                sleep(2)
            else:
                break
    except Exception:
        traceback.print_exc()
def getPostsIDGroup(driver, idGroup, numberPost=100):
    try:
        driver.get('https://mbasic.facebook.com/groups/' + str(idGroup))
        sleep(2)
        sumLinks = readDataFileITxtID(fileGroupID)
        while (len(sumLinks) < numberPost):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                likeBtn = driver.find_elements(By.XPATH, '//*[contains(@id, "like_")]')
                if len(likeBtn):
                    for id in likeBtn:
                        idPost = id.get_attribute('id').replace("like_", "")
                        if (idPost not in sumLinks and len(sumLinks) < numberPost):
                            sumLinks.append(idPost)
                            writeFileTxtID(fileGroupID, idPost)
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
    except Exception:
        traceback.print_exc()
def getPostIDFanpage(driver, idGroup, numberpost=100):
    try:
        driver.get("https://mbasic.facebook.com/" + str(idGroup));
        sleep(2)
        # địa chỉ URL hiện tại
        current_url = driver.current_url
        # lấy tên người dùng
        nameUser = current_url.split("/")[-1]
        timeline = driver.find_element(By.XPATH, "//a[starts-with(@href, '/" + nameUser + "?v=timeline')]")
        timeline.click()
        sleep(2)
        sumLinks = readDataFileITxtID(fileFanpageID)
        while (len(sumLinks) < numberpost):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                likeBtn = driver.find_elements(By.XPATH, '//*[contains(@id, "like_")]')
                if len(likeBtn):
                    for id in likeBtn:
                        idPost = id.get_attribute('id').replace("like_", "")
                        if (idPost not in sumLinks and len(sumLinks) <= numberpost):
                            sumLinks.append(idPost)
                            writeFileTxtID(fileFanpageID, idPost)
                nextBtn = driver.find_elements(By.XPATH, '//a[contains(@href, "?cursor=")]')
                if (len(nextBtn)):
                    nextBtn[0].click()
                    sleep(2)
                else:
                    break
            except WebDriverException:
                traceback.print_exc()
    except Exception:
        traceback.print_exc()
def getContentFromPostID(driver, postID):
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        contentBox = soup.find('div', id='m_story_permalink_view')
        userLink = contentBox.find('header').find(
            lambda tag: tag.name == 'a' and tag.get('href', '').startswith('/profile.php'))
        if (userLink != None):
            userLink = userLink['href']
        content = contentBox.find('div', attrs={'data-ft': '{\"tn\":\"*s\"}'})
        imgGroup = contentBox.find('div', attrs={'data-ft': '{\"tn\":\"H\"}'})
        footer = contentBox.find('footer', attrs={'data-ft': '{\"tn\":\"*W\"}'})
        obj = {'IDPost': postID}
        if (userLink != None):
            obj['IDUserSend'] = userLink.split("?id=")[1].split("&")[0]
            obj['NameUserSend'] = userLink.get_text()
        if (content != None):
            obj['ContentPost'] = content.get_text()
        if (footer != None):
            obj['TimePost'] = footer.find('abbr').get_text()
        if(imgGroup != None):
            listHref = imgGroup.find_all('a', attrs={'href': lambda x: x and 'photo' in x})
            listimg = []
            if(listHref != None):
                listHref = ["https://www.facebook.com" + i['href'] for i in listHref]
                for href in listHref:
                    driver.get(href)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    img = soup.find('img', attrs={'data-visualcompletion': 'media-vc-image'})
                    if(img!= None):
                        listimg.append(img['src'])
            obj['LinkImg'] = ';'.join(listimg)
            obj['LinkPost'] = driver.current_url
        obj = {k : v for k, v in obj.items() if v != None and v != "" and v != []}
        return obj
    except Exception:
        traceback.print_exc()