
import requests
from bs4 import BeautifulSoup
import time

from scraper_base_util import BaseData, BaseData_Browser, Scraper_util

#############################################################################################################################################
### 定義爬下來的東西 長什麼樣子
class Day_info(BaseData):
    def __init__(self, title, url, date, author):
        # self.block_i = block_i ### 目前覺得不需要這個
        self.title = title
        self.url = url
        self.date = date
        self.author = author

    def __str__(self):
        return "\n".join([self.title, self.url, self.date, self.author])



class Day_infos(BaseData_Browser):
    def __init__(self, result_dir):
        self.day_infos = []            ### 建立 容器
        self.result_dir = result_dir   ### products 物件放哪裡
    
    def add_BaseData(self, title, url, date, author):
        self.day_infos.append( Day_info( title, url, date, author) )

    def read_BaseData_from_file(self, path):
        with open( path , "r" , encoding = "utf8") as f:
            details = {}
            for go_line, line in enumerate(f):
                if  ( (go_line+1)% 5 == 1 ): details["block_i"] = line.rstrip("\n")
                elif( (go_line+1)% 5 == 2 ): details["title"]   = line.rstrip("\n")
                elif( (go_line+1)% 5 == 3 ): details["url"]     = line.rstrip("\n")
                elif( (go_line+1)% 5 == 4 ): details["date"]    = line.rstrip("\n")
                elif( (go_line+1)% 5 == 0 ): details["author"]  = line.rstrip("\n")

                if( (go_line+1)% 5 == 0 ):
                    self.add_BaseData( **details )
                    del details
                    details = {}

class Ithelp_scraper_util(Scraper_util):
    @staticmethod
    def get_page_amount(in_url):
        res = requests.get(in_url) ### request 的 get 去向 server 提出get 來抓取 html
        res.encoding = 'utf8'      ### request 下來的html 要怎麼 encode
        soup = BeautifulSoup(res.text, "lxml")  ### parse request下來的html， 第二個參數是選擇parser，然後要記得 pip install lxml 喔！

        if(len(soup.select(".profile-pagination")[0].select("li"))<=0): ### 如果沒有 "上下一頁"的<li>， 代表只有1葉
            page_amount = 1
        else:  
            page_amount = int(soup.select(".profile-pagination")[0].select("li")[-2].text) ### "下一頁"的前一個<li> 就剛好是最後一頁的頁數

        return page_amount

    @staticmethod
    def get_page_element(in_url, containor):
        res = requests.get(in_url)  ### request 的 get 去向 server 提出get 來抓取 html
        res.encoding = "utf8"       ### request 下來的html 要怎麼 encode
        soup = BeautifulSoup(res.text, "lxml") ### parse request下來的html， 第二個參數是選擇parser，然後要記得 pip install lxml 喔！
        
        ### 算block_i 用的，但目前覺得不需要block_i所以先註解掉了~
        # if( len(soup.select(".active")) >0 ): page_index = int(soup.select(".active")[0].text) ### "下一頁"的前一個<li> 就剛好是最後一頁的頁數
        # else:                                 page_index = 1
        # print("page_index", page_index)
        
        for go_day, day_info_block in enumerate(soup.select((".qa-list"))):  ### go_day是算block_i 用的，但目前覺得不需要block_i所以先不理他~
            for day_info in day_info_block.select(".profile-list__content"):
                details = {}
                # details["block_i"]      = str(10*(page_index-1) + go_day) ### +1是因為Day從1開始算
                details["title"]    = day_info.select("a")[0].text.lstrip().rstrip()   ### 標題
                details["url"]      = day_info.select("a")[0].attrs["href"].lstrip().rstrip()   ### url
                details["date"]     = day_info.select(".qa-list__info")[0].select("a")[0].attrs["title"]   ### 日期
                details["author"]   = day_info.select(".qa-list__info")[0].select("a")[1].text.rstrip()   ### 作者

                containor.add_BaseData( **details)
                print(containor.day_infos[-1])

if(__name__=="__main__"):
    containor = Day_infos(result_dir = "")
    Ithelp_scraper_util.get_page_element(in_url = "https://ithelp.ithome.com.tw/users/20119971/ironman/2254?page=2", containor=containor)



