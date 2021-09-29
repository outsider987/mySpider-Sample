import requests
from bs4 import BeautifulSoup
import mysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ftp as MyFtp
import urllib
import urllib.request
import zlib
import time
import errorRecoder
from fake_useragent import UserAgent

import undetected_chromedriver as uc
import asyncio
from playwright.async_api import async_playwright
import random
import myfilter
from threading import Thread
import myProxy
from fp.fp import FreeProxy
import json
import os
import codecs

sleepSec = 2
base = "https://rouman5.com"


class MySpider:

    def __init__(self, url, proxies):
        self.rootUrl = url
        self.proxies = proxies
        self.playwr = async_playwright().start()
        self.headless = False

    async def start_requests(self):
        try:
            async with async_playwright() as p:
                # proxy = random.choice(self.proxies)
                fu = UserAgent(verify_ssl=False)
                headers = {'user-agent': fu.firefox,
                           #    'referer': 'https://ceomap.site/#/advertising#about'
                           }
                browser = await p.firefox.launch(
                    headless=self.headless,
                    timeout=1000 * 80,
                    # proxy={
                    #     "server": proxy
                    # }
                )

                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(self.rootUrl, timeout=1000 * 100, referer='https://www.youtube.com/')
                # here you need to redefine your want element class
                await page.wait_for_selector('ul.books_listArea__2YYEg ', timeout=1000 * 10)
                comicRoots = await page.query_selector_all('a.comicBox_link__2ZHYh')
                for comicRoot in comicRoots:
                    a_href = await comicRoot.get_attribute('href')
                    await self.enterRoot(base+a_href)
                # test = await page.query_selector('text=福利媛')
                await page.click('a.comicBox_link__2ZHYh')
                await page.click('text=福利媛')
                await self.start_requests()
                # await page.close()
                # await browser.close()
                # await context.close()

        except Exception as e:
            print(e)
            page.close()
            browser.close()
            context.close()
            del page
            del browser
            del context
            await self.start_requests()

    async def enterRoot(self, a_href):
        async with async_playwright() as playwright2:
            fu = UserAgent(verify_ssl=False)
            headers = {'user-agent': fu.firefox,
                       #    'referer': 'https://ceomap.site/#/advertising#about'
                       }
            browser = await playwright2.firefox.launch(
                headless=self.headless,
                timeout=1000 * 80,
                # proxy={
                #     "server": proxy
                # }
            )
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(a_href, timeout=1000 * 100, referer='https://www.youtube.com/')
            await page.wait_for_selector('div.bookid_chapterBox__CRrx9', timeout=1000 * 10)
            comics = await page.query_selector_all('div.bookid_chapter__20FJi')
            for comicRoot in comics:
                a_href = await comicRoot.get_attribute('href')
                await self.enterRoot(a_href)
