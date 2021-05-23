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

import undetected_chromedriver as uc
import asyncio
from playwright.sync_api import sync_playwright
import random
import myfilter
from threading import Thread
import myProxy
from fp.fp import FreeProxy

# eventlet.monkey_patch(socket=True, select=True)



base = 'https://18comic.org'
cloulfare = "https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
sleepSec = 2


# headers = {'user-agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
#     }
payload = {'as_epq': 'James Clark', 'tbs': 'cdr:1,cd_min:01/01/2015,cd_max:01/01/2015', 'tbm': 'nws'}
user_agent = UserAgent()
class MySpider:
    
    def __init__(self, url,proxies):
        self.rootUrl = url
        self.proxies = proxies
        self.playwr = sync_playwright().start()
        self.headless = False
        # eventlet.monkey_patch(socket=True, select=True)
        # monkey.patch_all()

    def get_browser_Page_WithProxy(self):
        # proxy  = random.choice(self.proxies)
        browser = self.playwr.firefox.launch(
            headless=self.headless,
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
                headless=self.headless,
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
            page.goto(self.rootUrl,timeout=1000 * 100)
            # page.wait_for_timeout(10000)
            page.wait_for_selector('div.thumb-overlay-albums > a',timeout=1000 * 80)
            
            ComicMain_Tags = page.query_selector_all('div.thumb-overlay-albums > a')
            ComicMain_Images  = page.query_selector_all('div.thumb-overlay-albums > a > img')
            
            # start set threads
            threads = []
            for index, ComicMain_Tag in enumerate(ComicMain_Tags, start=0):
                a_href =  ComicMain_Tag.get_attribute('href')
                url = base + a_href
                thumbnail_url = ComicMain_Images[index].get_attribute('data-original')
                self.rootComicRequest(url, thumbnail_url)
                # thread = Thread(target=self.rootComicRequest,args=(url, thumbnail_url)) 
                # threads.append(thread)
                # thread.start()
            # for thread in threads:
            #     thread.join()

            nextrequest_Tags = page.query_selector_all('ul.pagination > li > a')
            nextrequest_url = nextrequest_Tags[len(nextrequest_Tags) - 1].get_attribute('href').strip()
            page.close()
            self.rootUrl = nextrequest_url
            self.start_requests()
            print('wa are request next'+nextrequest_url)
        except Exception as e:
            page.close()
            browser.close()
            context.close()
            del page
            del browser
            del context

            self.start_requests()

            print(e)
    def test(self,i):
        print(i)
        

    def rootComicRequest(self, rootComicurl, thumbnail_url):
        try:
            # playwr = sync_playwright().start()
            # proxyt = FreeProxy().get()
            # work = False
            # while work==False:
            #     work = myProxy.check_proxy(proxyt)
            #     if work==False:
            #         proxyt = FreeProxy().get() 
            proxy  = random.choice(self.proxies)
            browser = self.playwr.firefox.launch(
                headless=self.headless,
                timeout=1000 * 80,
                proxy={
                    "server":proxy
                }
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
            # page = self.get_browser_Page_WithProxy()
            page.goto(rootComicurl, timeout=1000 * 60)
            page.wait_for_load_state
            page.wait_for_selector('div.thumb-overlay-albums > a')
            print(page.content)
            com_a_list = page.query_selector_all('ul.btn-toolbar  a')
            
            comicMainIndexData = ''
            comicMainIndexNumData = ''
            comicMainIndexData = page.query_selector(
            'div.row > div.col-lg-7 > div > div.p-t-5').inner_text()
            # index comic
            comicMainIndexData = OnlyCharNum(comicMainIndexData)
            comicMainIndexNumData = OnlyNum(comicMainIndexData)

            comicDescData = ''
            desc = ''
            link = ''

            comicDescData = page.query_selector_all(
            'div.p-t-5')
            desc = comicDescData[10].inner_text()
            
            link = rootComicurl

            title = ''
            comicTitleData = page.query_selector(
            'div.pull-left > h1')
            title = comicTitleData.inner_text()

            comicGenreDataALL_element = page.query_selector('text=標籤：')
            comicGenreDataALL = comicGenreDataALL_element.query_selector_all('a')
            comicGenreDataALL_str = []
            for strdata in comicGenreDataALL:      
                comicGenreDataALL_str.append(strdata.inner_text())
            
            comicAuthor_element = page.query_selector('text=作者：')
            comicAuthorALL = comicGenreDataALL_element.query_selector_all('a')
            comicAuthor_str = []
            for strdata in comicAuthorALL:      
                comicAuthor_str.append(strdata.inner_text())

        #   store data for author and genre
            thumbnail_name = comicMainIndexNumData + ".jpg"
            mysql.storeRootComicsData(comicMainIndexData, comicMainIndexNumData, desc, rootComicurl, title, thumbnail_name,thumbnail_url)
            # self.save_img(thumbnail_name, comicMainIndexNumData, thumbnail_url)
            for genre in comicGenreDataALL_str:
                mysql.storeGenre(genre, comicMainIndexNumData)
            for author in comicAuthor_str:
                mysql.storeAuthor(author, comicMainIndexNumData)    
            

            comics_url_list = []
            for tag_a in com_a_list:
                a_href =  tag_a.get_attribute('href')
                url = base + a_href
                comics_url_list.append(url)
            
            # set thread and run
            threads = []
            comics_url_list = set(comics_url_list)
            comics_url_list = list(comics_url_list)
            comics_url_list = myfilter.filter_Path(comics_url_list)
            if len(comics_url_list) == 0:
                browser.close()
                page.close()
                context.close()
                del page
                del browser
                del context
                return
            for index , url in enumerate(comics_url_list,start=0):
                # time.sleep(sleepSec)
                # self.comics_parse(url, comicMainIndexNumData,None,None)
                thread = Thread(target=self.comics_parse,args=(url, comicMainIndexNumData,proxy,None)) 
                threads.append(thread)
                print("we are in '%s' comic and we have '%s',comic will wait '%s' sec" % (index,len(comics_url_list),index))
                time.sleep(index)
                thread.start()
            for thread in threads:
                thread.join()

                page.close()
        except Exception as e:
            print(e)
            browser.close()
            page.close()
            context.close()
            del page
            del browser
            del context
            self.rootComicRequest(rootComicurl, thumbnail_url) 
            
       

    def comics_parse(self, comicUrl, comicMainIndexNumData,proxy,playwr):
        try:
            browser =None
            if playwr == None:
                playwr = sync_playwright().start()
                browser = playwr.firefox.launch(
                    headless=True,
                    timeout=1000 * 80,
                    proxy={
                        "server":proxy
                    }
                    )
            else:
                # proxy  = random.choice(self.proxies)
                browser = playwr.firefox.launch(
                    headless=True,
                    timeout=1000 * 80,

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
            page.goto(comicUrl, timeout=1000 * 60)
            testtest= page.query_selector_all('div.thumb-overlay-albums img')
            page.wait_for_selector('div.thumb-overlay-albums')
            imgThumbtags = page.query_selector_all('div.thumb-overlay-albums img')
            imgThumbtags_arrar = imgThumbtags.copy()
            imgThumbtags = myfilter.filter_imgurl(comicMainIndexNumData, imgThumbtags_arrar)
            if len(imgThumbtags) == 0:
                browser.close()
                page.close()
                context.close()
                del page
                del browser
                del context
                return
            # check we had canvas to insert data
            canvasExist = False

            canvas = page.query_selector('canvas')
            if canvas :
                canvasExist = True
            else:
                canvasExist = False    

            img_url_Arrary = []
            page_num_Arrary = []
            path_Array = []
            canvasExist_Arrary = []
            index = 0
            for index, imgThumbtag in enumerate(imgThumbtags, start=0):
                    
                if(imgThumbtag.get_attribute('id') != None):
                    page_num = imgThumbtag.get_attribute('id')
                    img_url = imgThumbtag.get_attribute('data-original')
                    tilteCategeoryNum = imgThumbtag.get_attribute('data-original').split('/')
                    path = tilteCategeoryNum[len(tilteCategeoryNum) - 2]

                    # check img is exist 
                    # if self.save_img(page_num, path, img_url):

                    path_Array.append(path)
                    page_num_Arrary.append(page_num)
                    canvasExist_Arrary.append(canvasExist)
                    img_url_Arrary.append(imgThumbtag.get_attribute('data-original'))
                    
                
                    index += 1
                else:
                    continue
                
            mysql.storeComics(page_num_Arrary, img_url_Arrary, path_Array, canvasExist_Arrary, comicMainIndexNumData)
            browser.close()
            page.close()
            context.close()
            del page
            del browser
            del context
            # del playwr
        except Exception as e:
            print(e)
            browser.close()
            page.close()
            context.close()
            # playwr.close()
            del page
            del browser
            del context
            # del playwr
          
            
            self.comics_parse(comicUrl, comicMainIndexNumData,proxy,playwr) 
            print(e)
       

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
            ua = UserAgent()
            headers = {'User-Agent': ua.random}
            # proxy = urllib.request.ProxyHandler({'http': random.choice(self.proxies)})
            req = urllib.request.Request(img_url, headers=headers)
            # test = random.choice(self.proxies)
            # req.set_proxy(test,'http')
            response = urllib.request.urlopen(req, timeout=300)

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
            error.append(img_name)
            error.append(enter_ftp_path)
            error.append(img_url)
            errorHanlder.saveErrorUrlToJson(error)
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

