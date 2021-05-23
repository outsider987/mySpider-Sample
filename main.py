# 
import os
import sys
# currentpath = os.getcwd()
# currentpath += '\ceoComic'
# sys.path.append(currentpath)
# from spider import MySpider
from spider_playwright import MySpider
# from spider_playwright2 import MySpider
import myProxy

cateGeoryListurl = [
    'https://18comic.org/albums/hanman'
    # ,
    # 'https://18comic.org/albums/doujin',
    # 'https://18comic.org/albums/single',
    # 'https://18comic.org/albums/short',
    # 'https://18comic.org/albums/another',
    
    # 'https://18comic.org/albums/meiman'
]


def main():
    for rootUrl in cateGeoryListurl:
        # proxies = myProxy.getWorking_proxy_arrary()
        proxies = ''
        # requset_proxies = proxy.toRequesyProxy(proxies)
        spider = MySpider(rootUrl,proxies)
        # spider = MySpider(rootUrl,proxies)
        spider.start_requests()


if __name__ == '__main__':
    main()
    


