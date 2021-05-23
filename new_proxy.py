# import urllib
# import urllib.request
# from fake_useragent import UserAgent
# ua = UserAgent()
# print(ua.random)
# headers={'user-agent':ua.random}
# req = urllib.request.Request('https://cdn-msp.18comic.org/media/photos/216936/00001.jpg?v=1620894799',headers=headers)
#             # test = random.choice(self.proxies)
#             # req.set_proxy(test,'http')
# response = urllib.request.urlopen(req, timeout=300)
# print(response)

from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests
import pandas as pd



def getProxy():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)

    IPPool = []
    for i in range(1,6):
        # 用迴圈逐一打開分頁
        url = 'http://free-proxy.cz/zh/proxylist/country/US/https/ping/all/{}'.format(i)
        print('Dealing with {}'.format(url))
        driver.get(url)
        soup = BeautifulSoup(driver.page_source)
        for j in soup.select('tbody > tr'):
            # 用正則表達式抓取IP
            if re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', str(j)):
                IP = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', str(j))[0]
                Port = re.findall('class="fport" style="">(.*?)</span>', str(j))[0]
                IPPool.append(pd.DataFrame([{'IP':IP, 'Port':Port}]))
        print('There are {} IPs in Pool'.format(len(IPPool)))
    IPPool = pd.concat(IPPool, ignore_index=True)
    ActIps = []
    for IP, Port in zip(IPPool['IP'],IPPool['Port']):
        proxy = {'http':'http://'+ IP + ':' + Port,
                'https':'https://'+ IP + ':' + Port} 
        try:
            # 隨機找的一篇新聞即可
            url = 'https://www.chinatimes.com/realtimenews/20200205004069-260408'
            resp = requests.get(url, proxies=proxy, timeout=2)
            if str(resp.status_code) == '200':
                ActIps.append(pd.DataFrame([{'IP':IP, 'Port':Port}]))
                print('Succed: {}:{}'.format(IP, Port))
            else:
                print('Failed: {}:{}'.format(IP, Port))
        except:
                print('Failed: {}:{}'.format(IP, Port))
    ActIps = pd.concat(ActIps, ignore_index=True)
    return ActIps
print(getProxy())
