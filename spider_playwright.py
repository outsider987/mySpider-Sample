import requests
from bs4 import BeautifulSoup
import mysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import  ftp as MyFtp
import urllib
import urllib.request
import zlib
import time
import errorRecoder
from fake_useragent import UserAgent

import undetected_chromedriver as uc
import asyncio
from playwright.sync_api import sync_playwright
import random
import myfilter
from threading import Thread
import myProxy
from fp.fp import FreeProxy
import json
import os
import codecs

sleepSec = 2
class MySpider:
    
    def __init__(self, url,proxies):
        self.rootUrl = url
        self.proxies = proxies
        self.playwr = sync_playwright().start()
        self.headless = False

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
            
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.rootUrl,timeout=1000 * 100)
            # here you need to redefine your want element class
            page.wait_for_selector('div.class',timeout=1000 * 80) 
            data_arrary = page.query_selector_all('div.class > a')
            
            page.close()
            browser.close()
            context.close()
            del page
            del browser
            del context

        except Exception as e:
            page.close()
            browser.close()
            context.close()
            del page
            del browser
            del context
            print(e)
    def save_json(json_arrary):
        storePath_name = os.getcwd() + '\\error.json'
        with codecs.open(storePath_name, 'a', encoding='UTF-8') as f:
            line = json.dumps(json_arrary, ensure_ascii=False) + '\n'
            f.write(line)
            f.close()

    def save_img(self, img_name, enter_ftp_path, img_url):
        print('star saving pic: ' + img_url)
        # locale store path  
        document = os.getcwd() + '\\image'
        # path nameing
        comics_path = document + '\\' + enter_ftp_path
        exists = os.path.exists(comics_path)

        if not exists:
            print('create document: ' + enter_ftp_path)
            os.makedirs(comics_path)
        # nameing image
        pic_name = comics_path + '\\' + img_name 

        # check we had img
        exists = os.path.exists(pic_name)
        if exists:
            print('pic exists: ' + pic_name)
            return False

        try:
            ua = UserAgent()
            headers = {'User-Agent': ua.random} 
            req = urllib.request.Request(img_url, headers=headers)
            response = urllib.request.urlopen(req, timeout=300)

            # reponse data
            data = response.read()

            # we need extract data use zip 
            if response.info().get('Content-Encoding') == 'gzip':
                data = zlib.decompress(data, 16 + zlib.MAX_WBITS)

            # 图片保存到本地
            fp = open(pic_name, "wb")
            fp.write(data)
            fp.close()
            print('save image finished:' + pic_name)
            return True
            # ftp write method
            
            # fpLocal = open(pic_name, 'rb')
            # ftp = MyFtp.ftpconnect('156.67.222.57', 'u565698326.topceo.online', 'T5204t5204')
            # return MyFtp.uploadftpfile(ftp, fpLocal, enter_ftp_path, img_name)

        except Exception as e:
            print('save image error.')
            print(e)
            error = []
            error.append(img_name)
            error.append(enter_ftp_path)
            error.append(img_url)
            errorRecoder.saveErrorUrlToJson(error)
            # fpLocal.close()
            # os.remove(pic_name)

