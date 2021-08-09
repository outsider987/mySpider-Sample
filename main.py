#
import os
import sys
# from spider_playwright import MySpider
from spider_playwright import MySpider
import myProxy
import asyncio
import nest_asyncio
# nest_asyncio.apply()
# your
targetUrl = 'https://ceomap.site/#/main'


def main():

    proxies = ""
    # proxies = myProxy.getWorking_proxy_arrary()
    # proxies = myProxy.convertToRequestPool(proxies)
    spider = MySpider(targetUrl, proxies)
    #
    # loop = asyncio.get_running_loop()

    # loop.run_until_complete(spider.start_requests(proxies))
    asyncio.run(spider.start_requests())
    # spider.start_requests()


if __name__ == '__main__':
    main()
