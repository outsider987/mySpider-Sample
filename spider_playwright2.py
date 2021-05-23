import requests
from bs4 import BeautifulSoup
import mysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import  ftp as MyFtp
import os
import urllib
import urllib.request
import zlib
import time
import errorHanlder
from fake_useragent import UserAgent
import  proxy

from lxml import html

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import asyncio
from playwright.sync_api import sync_playwright
import random
import json


base = 'https://18comic.org/'
cloulfare = "https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
sleepSec = 2

# headers = {'user-agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
#             'Cookie': 'cf_clearance=b70a193685b48db39e7aa675bebe23d6a38aee30-1620123254-0-150; __cfduid=db79e20663a8e86357efc0ecefdca26e21620123254; ipcountry=TW; AVS=tgtac8fv63q6o0ok5g9lm9hhh4; shunt=1; _gid=GA1.2.449183907.1620123255; _gat_ga0=1; _gat_ga1=1; cover=1; guide=1; ipm5=11b58b5505a6f49a5e670425078fe94a; _ga_YYJWNTTJEN=GS1.1.1620123254.1.1.1620123270.44; _ga=GA1.1.1483747990.1620123255',
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

payload = {'as_epq': 'James Clark', 'tbs': 'cdr:1,cd_min:01/01/2015,cd_max:01/01/2015', 'tbm': 'nws'}

class MySpider:
    
    def __init__(self, url,proxies):
        self.rootUrl = url
        self.proxies = proxies
        self.playwr = sync_playwright().start()
    
    def get_browser_Page_WithProxy(self):
            proxy  = random.choice(self.proxies)
            browser = self.playwr.firefox.launch(
                headless=False,
                timeout=1000 * 80,
                # proxy={
                #     "server":proxy
                # }
                )
            
            context = browser.new_context(
                # locale='en-US',
                # is_mobile=True,
                # viewport={ 'width': 1280, 'height': 1024 },
                # device_scale_factor=2,
                # timezone_id='Europe/Berlin',
                # geolocation={"longitude": 48.858455, "latitude": 2.294474},
                # permissions=["geolocation"],
                # color_scheme='dark',
                # user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
            
            )
            
            page = context.new_page()
            return page
    def start_requests(self):
        try:
            # proxy  = random.choice(self.proxies)
            browser = self.playwr.firefox.launch(
                headless=False,
                timeout=1000 * 80,
                # proxy={
                #     "server":proxy
                # }
                )
            user_agent = UserAgent()
            agent = user_agent.firefox
            context = browser.new_context(
                # locale='en-US',
                # is_mobile=True,
                # viewport={ 'width': 1280, 'height': 1024 },
                # device_scale_factor=2,
                # timezone_id='Europe/Berlin',
                # geolocation={"longitude": 48.858455, "latitude": 2.294474},
                # permissions=["geolocation"],
                # color_scheme='dark',
                user_agent=agent
            
            )
            
            page = context.new_page()
    
            page.goto(self.rootUrl, timeout=1000 * 100)
            page.wait_for_selector('div.thumb-overlay-albums > a',timeout=1000 * 60)
            cookie1 = context.cookies()
           
            final_cookie = cookie1[0]['name'] + '=' + cookie1[0]['value'] + ';'+cookie1[2]['name'] + '=' + cookie1[2]['value'] 
            spiltstr = page.url.split('?__')
            session = requests.Session()
            cookie = spiltstr[len(spiltstr)-1]
            # user_agent = UserAgent()
            headers = {'user-agent': agent,
                'Cookie': final_cookie,
                }
            prxoy_value = "http://" + random.choice(self.proxies)
            prxoy = dict(http = prxoy_value)
            rootResp = requests.post(url=self.rootUrl, headers=headers, proxies=prxoy)

            while rootResp.status_code != 200:
                prxoy_value = "http://" + random.choice(self.proxies)
                prxoy = dict(http = prxoy_value)
                rootResp = requests.post(url=self.rootUrl, headers=headers, proxies=prxoy)
            rootResp.encoding = 'utf-8'
            
            print(rootResp.text)
            content = rootResp.content
            soup = BeautifulSoup(content, "html5lib")   
            ComicMain_Tags = soup.select('div.thumb-overlay-albums > a')
            ComicMain_Images = soup.select('div.thumb-overlay-albums > a > img')
            for index , ComicMain_Tag in enumerate(ComicMain_Tags, start=0):
                url = base + ComicMain_Tag['href']
                thumbnail_url = ComicMain_Images[index].get('data-original')
                self.rootComicRequest(url, thumbnail_url)
            nextrequest_Tags = soup.select('ul.pagination > li')
            nextrequest_url = nextrequest_Tags[len(nextrequest_Tags) - 1].find('a')['href'].strip()
        except Exception as e:
            page.close()
            self.start_requests()

            print(e)

    def rootComicRequest(self, rootComicurl, thumbnail_url):
        rootComicResp = requests.get(rootComicurl)
        rootComicResp.encoding = 'utf-8'
        content = rootComicResp.content
        soup = BeautifulSoup(content, "html5lib")
        com_a_list = soup.select('ul.btn-toolbar a')
        
        comicMainIndexData = ''
        comicMainIndexNumData = ''
        comicMainIndexData = soup.find(
        'div', class_='p-t-5 p-b-5').text.strip()
        # index comic
        comicMainIndexData = OnlyCharNum(comicMainIndexData)
        comicMainIndexNumData = OnlyNum(comicMainIndexData)

        comicDescData = ''
        desc = ''
        link = ''
        comicDescData = soup.find(
        'div', class_='col-xs-12 col-lg-7 nav-tab-content')
        desc = comicDescData.find_all('div', class_='p-t-5 p-b-5')[0].text 
        
        link = rootComicurl

        title = ''
        comicTitleData = soup.select(
        'div.pull-left > h1')
        title = comicTitleData[0].text

        comicGenreData = ''
        comicGenreDataALL = soup.find('span', itemprop="genre")
        comicGenreData = comicGenreDataALL.find_all('a', class_='btn btn-sm btn-primary')

        comicAuthor = ''
        comicAuthorALL = soup.find_all('div', class_='tag-block')
        tempAuthor = comicAuthorALL[3].find('a', class_='btn btn-sm btn-primary')
        if(tempAuthor != None):
            comicAuthor = comicAuthorALL[3].find('a', class_='btn btn-sm btn-primary').text
        # comicAuthor = comicAuthorALL.find('div', text="作者:")
        thumbnail_name = comicMainIndexNumData + ".jpg"
        mysql.storeRootComicsData(comicMainIndexData, comicMainIndexNumData, desc, rootComicurl, title, thumbnail_name)
        self.save_img(thumbnail_name, comicMainIndexNumData, thumbnail_url)
        for genre in comicGenreData:
            mysql.storeGenre(genre.text, comicMainIndexNumData)
        mysql.storeAuthor(comicAuthor, comicMainIndexNumData)

        comics_url_list = []
        for tag_a in com_a_list:
            url = base + tag_a['href']
            comics_url_list.append(url)
          
        for url in comics_url_list:
            time.sleep(sleepSec)
            self.comics_parse(url, comicMainIndexNumData)

    def comics_parse(self, comicUrl, comicMainIndexNumData):
        comicResp = requests.get(comicUrl)
        content = comicResp.content
        soup = BeautifulSoup(content, "html5lib")

        imgThumbtags = soup.select('div.thumb-overlay-albums img')
        # seleium
        options = Options()
        options.use_chromium = True
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-notifications")
        chrome = webdriver.Chrome('./chromedriver/chromedriver.exe', chrome_options=options)
        chrome.get(comicUrl)
        # check we had canvas to insert data
        canvasExist = False

        try:
            chrome.find_element_by_xpath("//canvas")
            canvasExist = True
        except :
            canvasExist = False
        chrome.close()
        img_url_Arrary = []
        page_num_Arrary = []
        path_Array = []
        canvasExist_Arrary = []
        index = 0
        for index, imgThumbtag in enumerate(imgThumbtags, start=0):
                
            if(imgThumbtag.get('id') != None):
                page_num = imgThumbtag.get('id')
                img_url = imgThumbtag.get('data-original')
                tilteCategeoryNum = imgThumbtag.get('data-original').split('/')
                path = tilteCategeoryNum[len(tilteCategeoryNum) - 2]

                # check url
                if self.save_img(page_num, path, img_url):

                    # here is image itm pipline
                   
                    # if canvasExist:
                    #     path = "hide_" + path

                    path_Array.append(path)
                    page_num_Arrary.append(page_num)
                    canvasExist_Arrary.append(canvasExist)
                    img_url_Arrary.append(imgThumbtag.get('data-original'))
                # ftp to do
            
                index += 1
            else:
                continue
            
        mysql.storeComics(page_num_Arrary, img_url_Arrary, path_Array, canvasExist_Arrary, comicMainIndexNumData)

    def save_img(self, img_name, enter_ftp_path, img_url):
        # 将图片保存到本地
        print('star saving pic: ' + img_url)
        # 保存漫画的文件夹
        document = os.getcwd() + '\\image'
        # document = ''
        # 每部漫画的文件名以标题命名
        comics_path = document + '\\' + enter_ftp_path
        remotepath = enter_ftp_path + '\\' + img_name 
        exists = os.path.exists(comics_path)
        if not exists:
            print('create document: ' + enter_ftp_path)
            os.makedirs(comics_path)

        # 每张图片以页数命名
        pic_name = comics_path + '\\' + img_name 

        # 检查图片是否已经下载到本地，若存在则不再重新下载
        exists = os.path.exists(pic_name)
        if exists:
            print('pic exists: ' + pic_name)
            return False

        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}

            req = urllib.request.Request(img_url, headers=headers)
            response = urllib.request.urlopen(req, timeout=30)

            # 请求返回到的数据
            data = response.read()

            # 若返回数据为压缩数据需要先进行解压
            if response.info().get('Content-Encoding') == 'gzip':
                data = zlib.decompress(data, 16 + zlib.MAX_WBITS)

            # 图片保存到本地
            fp = open(pic_name, "wb")
            fp.write(data)
            fp.close()
            print('save image finished:' + pic_name)
            return True
            # old write method
            
            # fpLocal = open(pic_name, 'rb')
            # # ftpObject = ftp.ftpconnect('156.67.222.57', 'u565698326.topceo.online', 'T5204t5204')
            # ftp = MyFtp.ftpconnect('156.67.222.57', 'u565698326.topceo.online', 'T5204t5204')
            # return MyFtp.uploadftpfile(ftp, fpLocal, enter_ftp_path, img_name)

        except Exception as e:
            print('save image error.')
            print(e)
            error = []
            error.append(img_name, enter_ftp_path, img_url)
            errorHanlder.saveErrorUrlToJson()
            # fpLocal.close()
            # os.remove(pic_name)


def OnlyCharNum(s, oth=''):
    s = s.lower()
    fomart = 'abcdefghijklmnopqrstuvwxyz0123456789'
    for c in s:
        if not c in fomart:
            s = s.replace(c, '')
    return s

    
def OnlyNum(s, oth=''):
    s = s.lower()
    fomart = '0123456789'
    for c in s:
        if not c in fomart:
            s = s.replace(c, '')
    return s

