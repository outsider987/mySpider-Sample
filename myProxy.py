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
    playwr = sync_playwright().start()
    browser = playwr.firefox.launch(
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
    page.goto(proxyurl,timeout=1000 * 100)
    page.wait_for_selector('btn3',timeout=1000 * 80)
    page.click('id =btn3')
    # chrome.find_element_by_id('btn3').click()
    proxy_pandas =pd.read_clipboard(header=None)
    proxy_Arrary = proxy_pandas.to_numpy()
    proxy_Arrary_flattern = proxy_Arrary.flatten()
    list_arrary = proxy_Arrary_flattern.tolist()
    page.close()
    browser.close()
    context.close()
    del     page
    del     browser
    del     context
    # chrome.close()
    # chrome.stop_client()
    # chrome.switch_to_alert().accept() 
    # chrome.close()
    return list_arrary
    # for proxy in proxy_Arrary:



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

def toRequesyProxy(proxy_array):
    strs = 'http://' + '{0}'
    
    resut_arrary = {"http": strs.format(i) for i in proxy_array}
    return resut_arrary
# proxy_array = ['1231','1231','1231']
# strs = 'http://' + '{0}'
# test ={}
# resut_arrary = dict(http = strs.format(i) for i in proxy_array)
    
# # resut_arrary = {"http": strs.format(i) for i in proxy_array}
# print(test)
# return resut_arrary
#Example run : echo -ne "192.168.1.1:231\n192.168.1.2:231" | python proxy_checkpy3-async.py
