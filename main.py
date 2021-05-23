# 
import os
import sys
from spider_playwright import MySpider
import myProxy

# your 
targetUrl ='https://18comic.org/albums/hanman'


def main():
    proxies = myProxy.getWorking_proxy_arrary()
    spider = MySpider(targetUrl,proxies)
    spider.start_requests()


if __name__ == '__main__':
    main()
    


