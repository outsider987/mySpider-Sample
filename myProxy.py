import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import win32clipboard
import random
import urllib.request
import socket
from threading import Thread
import datetime
# from Tkinter import Tk
from playwright.async_api import async_playwright
import json
import sys
import asyncio
proxyurl = "https://www.proxy-list.download/HTTP"


async def getCrawleProxyPool_ArrAry():

    async with async_playwright() as p:
        browser = await p.firefox.launch(
            headless=False,
            timeout=1000 * 80,

        )

        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(proxyurl, timeout=1000 * 100)
        # here you need to redefine your want element class
        await page.wait_for_selector('#btn3', timeout=1000 * 80)
        await page.click("#btn3")
        proxy_pandas = pd.read_clipboard(header=None)
        proxy_Arrary = proxy_pandas.to_numpy()
        proxy_Arrary_flattern = proxy_Arrary.flatten()
        list_arrary = proxy_Arrary_flattern.tolist()

        return list_arrary


def check_proxy_returnArrary(pip, working_proxy_array):
    try:
        proxy_handler = urllib.request.ProxyHandler({'https': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        start = datetime.datetime.now()
        sock = urllib.request.urlopen(
            'https://outsider5987.blogspot.com/2021/03/3-beautifulsoup-find-select-findall.html')
        end = datetime.datetime.now()
        delta = end - start  # change
        # the url address here
        elapsed_seconds = round(delta.microseconds * .000001, 6)
        print(elapsed_seconds)
        print(pip + "is ok and append")
        working_proxy_array.append(pip)
        sock.close()
        proxy_handler.close()
        opener.close()

    except Exception as e:
        print(e)
        return True


def check_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        start = datetime.datetime.now()
        sock = urllib.request.urlopen(
            'https://outsider5987.blogspot.com/2021/03/3-beautifulsoup-find-select-findall.html')
        end = datetime.datetime.now()
        delta = end - start  # change
        # the url address here
        elapsed_seconds = round(delta.microseconds * .000001, 6)
        print(elapsed_seconds)
        print(pip + "is ok and append")
        sock.close()
        proxy_handler.close()
        opener.close()
        return True

    except Exception as e:
        print(e)
        return False


def getWorking_proxy_arrary():
    # setting time out
    socket.setdefaulttimeout(30)
    working_proxy_array = []
    proxies = asyncio.run(getCrawleProxyPool_ArrAry())
    threads = []

    for proxy in proxies:
        thread = Thread(target=check_proxy_returnArrary,
                        args=(proxy.strip(), working_proxy_array))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    del threads
    # time.sleep(5)
    thread.do_run = False
    return working_proxy_array


def convertToRequestPool(arrary):
    arrary1 = []
    arrary1 = arrary

    arrary2 = {"http": "http://"+i for i in (arrary1)}
    # arrary2 = json.dumps(test)

    # arrary2 = Convert(test)
    return arrary2


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct
