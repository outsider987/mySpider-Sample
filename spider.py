import requests
from bs4 import BeautifulSoup
import mysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ftp as MyFtp
import os
import urllib
import urllib.request
import zlib
import time
import errorRecoder
from fake_useragent import UserAgent
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import asyncio
from playwright.sync_api import sync_playwright
import json
import os
import codecs
import random

base = 'https://ceomap.site/#/main'
sleepSec = 2
# define your header


class MySpider:

    def __init__(self, url, proxies):
        self.rootUrl = url
        self.proxies = proxies

    def start_requests(self):
        try:
            fu = UserAgent(verify_ssl=False)
            headers = {'user-agent': fu.firefox,
                       'referer': 'https://ceomap.site/#/advertising#about'
                       }
            session = requests.Session()

            rootResp = requests.get(
                url=self.rootUrl, headers=headers, proxies=proxies)
            rootResp.encoding = 'utf-8'
            # respone
            content = rootResp.content
            soup = BeautifulSoup(content, "html5lib")
            element_data = soup.select('div.class')
            print(element_data)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

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
