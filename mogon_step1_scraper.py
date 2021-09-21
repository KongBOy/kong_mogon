import requests
from bs4 import BeautifulSoup
import time

import sys
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from build_dataset_combine import Check_dir_exist_and_build

from scraper_base_util import BaseData, Scraper_util, BaseData_Browser


import urllib3
urllib3.disable_warnings()
#############################################################################################################################################
### 定義爬下來的東西 長什麼樣子
class Product(BaseData):
    def __init__(self, prod_title, price, prod_url, img_url, shop_name):
        self.prod_title = prod_title
        self.price = price
        self.prod_url = prod_url
        self.img_url = img_url
        self.shop_name = shop_name

    def __str__(self):
        return "\n".join([self.prod_title, self.price, self.prod_url, self.img_url, self.shop_name])


class Products(BaseData_Browser):
    # def __init__(self, base_url, result_dir):
    def __init__(self, result_dir):
        self.prods = []            ### 建立 容器

        self.result_dir = result_dir   ### products 物件放哪裡
        self.result_imgs_dir = self.result_dir + "/imgs"   ### products的imgs 放哪裡

    def add_BaseData(self, prod_title, price, prod_url, img_url, shop_name):
        self.prods.append( Product(prod_title, price, prod_url, img_url, shop_name) )

    def read_BaseData_from_file(self, path):
        with open( path , "r" , encoding = "utf8") as f:
            details = {}
            for go_line, line in enumerate(f):
                if  ( (go_line+1)% 5 == 1 ): details["prod_title"] = line.rstrip("\n")
                elif( (go_line+1)% 5 == 2 ): details["price"]      = line.rstrip("\n")
                elif( (go_line+1)% 5 == 3 ): details["prod_url"]   = line.rstrip("\n")
                elif( (go_line+1)% 5 == 4 ): details["img_url"]   = line.rstrip("\n")
                elif( (go_line+1)% 5 == 0 ): details["shop_name"]   = line.rstrip("\n")

                if( (go_line+1)% 5 == 0 ):
                    self.add_BaseData( **details )
                    del details
                    details = {}


#############################################################################################################################################
class Mogon_Scraper_util(Scraper_util):
    @staticmethod
    def get_page_amount(in_url):
        res = requests.get(in_url, verify=False)  ### request 的 get 去向 server 提出get 來抓取 html
        res.encoding = 'utf8'       ### request 下來的html 要怎麼 encode
        soup = BeautifulSoup(res.text, "lxml")  ### parse request下來的html， 第二個參數是選擇parser，然後要記得 pip install lxml 喔！

        if(len(soup.select(".pages")) <= 0):  ### 如果不存在 .pages，代表找不到商品
            print("找不到商品，0頁")
            page_amount = 0
        else:  ### 如果存在 .pages，代表有找到商品，例如：http://www.moganshopping.com/zh_tw/public/search/searchitem.php?keyword=%E5%8C%85%E8%A3%B9%E5%A4%A7%E5%A4%A7&SearchMethod=multi&action=jyahooshopping
            product_amount = int(soup.select(".pages")[0].select(".page_info")[0].text[:-1])
            if(product_amount <= 30):  ### 如果 商品數 <= 30 只有一頁，頁尾<a>不會出現喔，直接手動指定頁數為1！例如：http://www.moganshopping.com/zh_tw/public/search/searchitem.php?keyword=%E5%8C%85%E8%A3%B9%E5%A4%A7&SearchMethod=multi&action=jyahooshopping
                page_amount = 1
            else:  ### 如果 商品數 > 30 才會有頁尾<a>出現喔！例如：http://www.moganshopping.com/zh_tw/public/search/searchitem.php?keyword=%E5%8C%85%E8%A3%B9&SearchMethod=multi&action=jyahooshopping
                # print( int(soup.select('.pages')[0].select("a")[-1].attrs['href'].split("=")[-1]) )
                page_amount = int(soup.select('.pages')[0].select("a")[-1].attrs['href'].split("=")[-1])
        return page_amount

    @staticmethod
    def get_page_element(in_url, products):
        res = requests.get(in_url, verify=False)  ### request 的 get 去向 server 提出get 來抓取 html
        res.encoding = "utf8"       ### request 下來的html 要怎麼 encode
        soup = BeautifulSoup(res.text, "lxml")  ### parse request下來的html， 第二個參數是選擇parser，然後要記得 pip install lxml 喔！

        # prods = []
        for prod in soup.select("#SIL_block"):
            for detail in prod.select("#SIL_item"):
                details = {}
                details["prod_title"] = detail.select('span')[2].text
                # details.append(detail.select('a')[1].select('span')[0].text)
                details["price"]    = detail.select('.red')[1].select('span')[2].text
                details["prod_url"] = detail.select('a')[0].attrs['href']
                details["img_url"]  =detail.select('img')[0].attrs['src']
                
                if(len(detail.select('a')) >= 3 ) : details["shop_name"]  = detail.select('a')[2].text  ### 正常<a>應該有4個，且店家會在第3個<a>
                else:                               details["shop_name"]  = detail.select('a')[0].text  ### 違禁品<a>只有兩個，且店家會在第1個<a>
                # print("a_amount", len(detail.select('a')), details["shop_name"])
                products.add_BaseData( **details )
        

    ##########################################################################################################################################
    @staticmethod
    def get_prods_image(products, start_index=0, main_log=None, prod_num=True, shop_name=False, price=False, prod_title=False):
        from urllib.request import urlopen
        for go_prod, prod in enumerate(products.prods[start_index:]):
            ### 去網路上 抓影像囉！
            img_byte = urlopen(prod.img_url)

            ### 決定要存哪裡
            ### 1.決定img_name
            img_name = ""
            if(prod_num): img_name = "%04i" % (go_prod + 1)  ### 最基本純流水號
            if(shop_name or prod_title or prod_title):
                if(shop_name):    img_name += f"_{ prod.shop_name }"       ### 加shop_name
                if(price):      img_name += f"_{ prod.price }"
                if(prod_title): img_name += f"_{ prod.prod_title }"    ### 加prod_title
                if(len(img_name) > 120): img_name =  img_name[:120]    ### 怕img_name太長！
                img_name = Mogon_Scraper_util.filte_invalid_symbol( img_name )  ### 去除 不能命名的符號
            if(img_name == ""): img_name = "%04i" % (go_prod + 1)  ### 防呆，以避免 prod_num, prod_num, shop_name 全為 False
            img_name += ".jpg"

            ### 2.決定img_sub_dir
            img_sub_dir = ""
            if(shop_name or prod_title or prod_title):
                img_sub_dir += "have"
                if(prod_num):   img_sub_dir += "-num"       ### 加shop_name
                if(shop_name):    img_sub_dir += "-shop_name"       ### 加shop_name
                if(price):      img_sub_dir += "-price"
                if(prod_title): img_sub_dir += "-title"    ### 加prod_title
            Check_dir_exist_and_build(products.result_imgs_dir + "/" + img_sub_dir)

            ### 3.根據 img_name 和 img_sub_dir 設定 img_path
            img_path = products.result_imgs_dir + "/" + img_sub_dir + "/" + img_name

            ### 4.把 圖片根據 img_path 存起來
            with open( img_path, "wb") as f:
                print(f"{go_prod}/{len(products.prods[start_index:])} download to " + img_path )
                f.write(img_byte.read())

            ### 怕抓太快被擋
            if( (go_prod  + 1) % 50 == 0 ): time.sleep(8)
