# 爬蟲7-棄坑Scrapy框架(request)

在開發到一半的爬蟲突然覺得Scrapy的彈性有點低,所以就立馬轉彎了

![%E7%88%AC%E8%9F%B27-%E6%A3%84%E5%9D%91Scrapy%E6%A1%86%E6%9E%B6(request)%204340e87e284e4dc88e76d6acd7196612/Untitled.png](%E7%88%AC%E8%9F%B27-%E6%A3%84%E5%9D%91Scrapy%E6%A1%86%E6%9E%B6(request)%204340e87e284e4dc88e76d6acd7196612/Untitled.png)

## Scrapy缺點:

1.在yield資料的時候,只能擇一pipline來做資料的存取,假如我要ftp跟sql跟json只能擇一來做資料的存取
2.本身的功能還有些bug 是你無法去修復的
3.開發的彈性太差,不好擴充功能,必須照著官方檔案來實作

## [MySpider:](https://github.com/outsider987/mySpider-Sample)

最後決定用最原始的方式來爬蟲,而這是我專案的結構

```powershell
C:.
└───mySpider-Sample
    │   .gitattributes
    │   .gitignore
    │   .gitignore.swp
    │   chromedriver.exe
    │   errorRecoder.py
    │   ftp.py
    │   main.py
    │   myfilter.py
    │   myProxy.py
    │   mysql.py
    │   README.md
    │   requirements.txt
    │   spider.py
    │   spider_playwright.py
    │
    └───chromedriver
            chromedriver.exe
```

## 主項:

**a.spider:**

1.主要是request搭配beautifulsoup

2.有存json以及圖片的功能

3.有限制防爬蟲的網站,目前沒有好的解決辦法

**b.spider_playwright:**

1.以playwright為主體

2.有存json以及圖片的功能

3.模擬器叫起瀏覽器方式

**c.mysql:**

1.存取sql的方法可以寫在這裡

2.我有寫一個getData的功能,(可以自行擴充喔)

3.擴充sql方法都可以寫在這裡

**d.main:**

程式的起始點

**e.myproxy:**

1.爬取免費的proxy

2.經過multiple threads 驗證過拿的proxy都是活的,品質的話則不一定

**f.myfilter:**

1.透過跟sql要資料去排除重複性的資料

```python
# here is get sql data to check it's existed it will remove duplicate data
def filter_imgurl(rootComics_mainIndex,src_arrary):

	set_arrary_data = mysql.getData('target_row_name', 'tablename', 'where_row_name', 'where_row_value')
	
	subset_arrary_data = set(set_arrary_data)
	
	result = [url for url in src_arrary if url not in set_arrary_data]
	
	copy_result = result.copy()
	
	# here is remove duplicate data
	
	for index,item in enumerate(result, start=0) :
	
		if item.get_attribute('id') == None:
	
		copy_result.remove(item)
	
	return copy_result
```

**g.errorRecoder:**

1.失敗的資料會寫進json裡,

2.可以知道哪些資料遺漏了

**h.ftp還未完成**

## 環境安裝:

1.python 3.9 

2.cmd install

```powershell
pip install .\requirements.txt
```

安裝playwright 模擬器 driver

```powershell
python -m playwright install
```

3.主程式

如果不想要用proxy,可以把它拿掉或是給他None值就可以了

```powershell
import os
import sys

from spider_playwright import MySpider

import myProxy

# your

targetUrl ='https://outsider5987.blogspot.com/2021/04/5-seleium.html'

def main():

	proxies = myProxy.getWorking_proxy_arrary()
	
	spider = MySpider(targetUrl,proxies)
	
	spider.start_requests()

if __name__ == '__main__':

	main()
```

## 小節:

這個爬蟲主要拉出架構來放置所需的程式碼,大部分的code 都必須寫在spider 或是**spider_playwright,**因為爬蟲還是蠻客製化的,但我把sql,ftp,還有spider都分開來,這樣在管理這些程式碼,會比較好管理一點,如果你覺得我的文章或是git不錯的話幫我github按顆星我會很感謝你的

# Github Link:

[https://github.com/outsider987/mySpider-Sample](https://github.com/outsider987/mySpider-Sample)

![%E7%88%AC%E8%9F%B27-%E6%A3%84%E5%9D%91Scrapy%E6%A1%86%E6%9E%B6(request)%204340e87e284e4dc88e76d6acd7196612/Untitled%201.png](%E7%88%AC%E8%9F%B27-%E6%A3%84%E5%9D%91Scrapy%E6%A1%86%E6%9E%B6(request)%204340e87e284e4dc88e76d6acd7196612/Untitled%201.png)

![%E7%88%AC%E8%9F%B27-%E6%A3%84%E5%9D%91Scrapy%E6%A1%86%E6%9E%B6(request)%204340e87e284e4dc88e76d6acd7196612/Untitled%202.png](%E7%88%AC%E8%9F%B27-%E6%A3%84%E5%9D%91Scrapy%E6%A1%86%E6%9E%B6(request)%204340e87e284e4dc88e76d6acd7196612/Untitled%202.png)
