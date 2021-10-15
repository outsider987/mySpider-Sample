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
# import myProxy
# from fp.fp import FreeProxy
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

                nextalls = await page.query_selector_all('a.btn-outline-primary')
                nextHref = await nextalls[nextalls.__len__()-1].get_attribute('href')
                await page.goto(base + nextHref, timeout=1000 * 100, referer='https://www.youtube.com/')

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
            pTags = await page.query_selector_all('p')
            title_h5 = await page.query_selector('h5')
            thumbnail_urlTag = await page.query_selector('div.comicBox_thumbImg__1aomD')
            thumbnail_url = await thumbnail_urlTag.get_attribute('data-src')
            title = await title_h5.inner_text()
            print(title)
            rootStr = []
            for index, p in enumerate(pTags):
                if index < 4:
                    text = await p.inner_text()
                    ptext = text.split(':')
                    rootStr.append(ptext[1])
            print(rootStr)
            descr = rootStr[3]
            author = rootStr[0].strip()
            status = rootStr[1]
            genre = rootStr[2]

            mysql.storeRootComicsData(
                descr, a_href, title, author, status, thumbnail_url)

            rouman_id_arrary = mysql.getData(
                'id', 'rouman_rootcomics', 'title', title)
            rouman_id = rouman_id_arrary[0]
            mysql.storeGenreData(rouman_id, genre)
            comics = await page.query_selector_all('div.bookid_chapter__20FJi')

            comics = myfilter.filter_chapter(rouman_id, comics)
            for index, comic in enumerate(comics):
                comic_a_Tag = await comic.query_selector('a')
                comic_href = await comic_a_Tag.get_attribute('href')
                await self.enterComics(base + comic_href, rouman_id, index)

    async def enterComics(self, comic_href, rouman_rootcomics_id, chapter):
        async with async_playwright() as playwright3:
            fu = UserAgent(verify_ssl=False)
            headers = {'user-agent': fu.firefox,
                       #    'referer': 'https://ceomap.site/#/advertising#about'
                       }
            browser = await playwright3.firefox.launch(
                headless=self.headless,
                timeout=1000 * 80,
                # proxy={
                #     "server": proxy
                # }
            )
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(comic_href, timeout=1000 * 100, referer='https://www.youtube.com/')
            await page.wait_for_selector('img.id_comicImage__2vwcn', timeout=1000 * 80)
            comics = await page.query_selector_all('img.id_comicImage__2vwcn')

            img_list = []
            for comic in comics:
                await comic.hover()
                comicImg_href = await comic.get_attribute('src')

                img_list.append(comicImg_href)

            mysql.storeComicsData(rouman_rootcomics_id, img_list, chapter)
