# 
import os
import sys
from spider_playwright import MySpider
import myProxy

# your 
targetUrl ='https://outsider5987.blogspot.com/2021/04/5-seleium.html'


def main():
    proxies = myProxy.getWorking_proxy_arrary()
    spider = MySpider(targetUrl,proxies)
    spider.start_requests()


if __name__ == '__main__':
    main()
    


