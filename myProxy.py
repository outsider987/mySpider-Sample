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
from playwright.sync_api import sync_playwright

proxyurl = "https://www.proxy-list.download/HTTP"

def getCrawleProxyPool_ArrAry():
    options = Options()
    options.use_chromium = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument('--headless')
    options.add_argument("--disable-notifications")
    chrome = webdriver.Chrome('./chromedriver/chromedriver.exe', chrome_options=options)
    chrome.get(proxyurl)

    # win32clipboard.OpenClipboard()
    chrome.find_element_by_id('btn3').click()
    proxy_pandas =pd.read_clipboard(header=None)
    proxy_Arrary = proxy_pandas.to_numpy()
    proxy_Arrary_flattern = proxy_Arrary.flatten()
    list_arrary = proxy_Arrary_flattern.tolist()
    
    chrome.switch_to_alert().accept() 
    chrome.close()
    return list_arrary



def check_proxy_returnArrary(pip,working_proxy_array):
    try:        
        proxy_handler = urllib.request.ProxyHandler({'https': pip})        
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        start = datetime.datetime.now()   
        sock = urllib.request.urlopen('https://outsider5987.blogspot.com/2021/03/3-beautifulsoup-find-select-findall.html')
        end = datetime.datetime.now()
        delta = end - start  # change
        elapsed_seconds = round(delta.microseconds * .000001, 6) #the url address here
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
        sock = urllib.request.urlopen('https://outsider5987.blogspot.com/2021/03/3-beautifulsoup-find-select-findall.html')
        end = datetime.datetime.now()
        delta = end - start  # change
        elapsed_seconds = round(delta.microseconds * .000001, 6) #the url address here
        print(elapsed_seconds)
        print(pip + "is ok and append")
        sock.close()
        proxy_handler.close()
        opener.close()
        return  True
        
    except Exception as e:        
        print(e)
        return False

def getWorking_proxy_arrary():
    # setting time out 
    socket.setdefaulttimeout(30)
    working_proxy_array =[]
    proxies = getCrawleProxyPool_ArrAry()
    threads = []

    for proxy in proxies:
        thread = Thread( target=check_proxy_returnArrary, args=(proxy.strip(), working_proxy_array))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    return working_proxy_array
