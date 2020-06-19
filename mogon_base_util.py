import requests
from bs4 import BeautifulSoup
import time

import sys 
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from build_dataset_combine import Check_dir_exist_and_build, Check_dir_exist_and_build_new_dir

from abc import abstractmethod

class Product:
    def __init__(self, prod_title, price, prod_url, img_url, shop_id):
        self.prod_title = prod_title
        self.price = price
        self.prod_url = prod_url
        self.img_url = img_url
        self.shop_id = shop_id

    def __str__(self):
        return "\n".join([self.prod_title, self.price, self.prod_url, self.img_url, self.shop_id])


### 這是一個 "操作Product介面"的概念~~~不實做，是給 需要操作product 的物件 繼承用的喔！實作部分在Products內，但是其實要把實作部分寫這裡好像也行，這樣其他ˊ口ˋ 再思考看看囉！
class ProductBrowser:
    @abstractmethod
    def read_prods_from_file(self, path): pass


class Products(ProductBrowser):
    def __init__(self):
        self.prods = []
    
    def add_prod(self, prod_title, price, prod_url, img_url, shop_id):
        self.prods.append( Product(prod_title, price, prod_url, img_url, shop_id) )

    def read_prods_from_file(self, path):
        with open( path , "r" , encoding = "utf8") as f:
            details = {}
            for go_line, line in enumerate(f):
                if  ( (go_line+1)% 5 == 1 ): details["prod_title"] = line.rstrip("\n")
                elif( (go_line+1)% 5 == 2 ): details["price"]      = line.rstrip("\n")
                elif( (go_line+1)% 5 == 3 ): details["prod_url"]   = line.rstrip("\n")
                elif( (go_line+1)% 5 == 4 ): details["img_url"]   = line.rstrip("\n")
                elif( (go_line+1)% 5 == 0 ): details["shop_id"]   = line.rstrip("\n")

                if( (go_line+1)% 5 == 0 ):
                    self.add_prod( **details )
                    del details
                    details = {}

class Get_all_page_util:
    def __init__(self):
        self.base_url = None
        self.products = None
        self.prods_dir = None
        self.prods_img_dir = None
        self.doc_dir = None

    def get_all_page_prods(self):
        page_amount = Scraper_util.get_page_amount(self.base_url)
        print("page_amount:",page_amount)
        page_amount = 2 ### debug用
        for go_page in range(page_amount):
            full_url = self.base_url +"&page="+ str(go_page+1) ### page是從1開始
            Scraper_util.get_page_prods( full_url, self.products )

            print(full_url + " read ok!!!!")
            with open(self.prods_dir +"/main_log.txt","a") as main_log: main_log.write(full_url + " read ok!!!! \n")
            if( (go_page+1)%10 ==0): time.sleep(5) ### 怕抓太快被擋，抓10頁休息5秒

    def get_all_page_prods_img(self, prod_title=False):
        if(self.products.prods == []) : self.get_all_page_prods() ### 如果 prods是空的，就先去抓 prods囉！
        Scraper_util.get_prods_image(self.products, self.prods_img_dir, start_index=0, prod_title=prod_title)


class Scraper_util:
    @staticmethod
    def filte_invalid_symbol(file_name):
        file_name = file_name.replace("\\", " ")
        file_name = file_name.replace("/", " ")
        file_name = file_name.replace(":", " ")
        file_name = file_name.replace("*", " ")
        file_name = file_name.replace("?", " ")
        file_name = file_name.replace('"', " ")
        file_name = file_name.replace("<", " ")
        file_name = file_name.replace(">", " ")
        file_name = file_name.replace("|", " ")
        return file_name 

    @staticmethod
    def get_page_amount(in_url):
        res = requests.get(in_url) ### request 的 get 去向 server 提出get 來抓取 html
        res.encoding = 'utf8'      ### request 下來的html 要怎麼 encode
        soup = BeautifulSoup(res.text, "lxml")  ### parse request下來的html， 第二個參數是選擇parser，然後要記得 pip install lxml 喔！

        if(len(soup.select(".pages"))<=0): ### 如果不存在 .pages，代表找不到商品
            print("找不到商品，0頁")
            page_amount = 0
        else:  ### 如果存在 .pages，代表有找到商品，例如：http://www.moganshopping.com/zh_tw/public/search/searchitem.php?keyword=%E5%8C%85%E8%A3%B9%E5%A4%A7%E5%A4%A7&SearchMethod=multi&action=jyahooshopping
            product_amount = int(soup.select(".pages")[0].select(".page_info")[0].text[:-1])
            if(product_amount <= 30): ### 如果 商品數 <= 30 只有一頁，頁尾<a>不會出現喔，直接手動指定頁數為1！例如：http://www.moganshopping.com/zh_tw/public/search/searchitem.php?keyword=%E5%8C%85%E8%A3%B9%E5%A4%A7&SearchMethod=multi&action=jyahooshopping
                page_amount = 1
            else: ### 如果 商品數 > 30 才會有頁尾<a>出現喔！例如：http://www.moganshopping.com/zh_tw/public/search/searchitem.php?keyword=%E5%8C%85%E8%A3%B9&SearchMethod=multi&action=jyahooshopping
                # print( int(soup.select('.pages')[0].select("a")[-1].attrs['href'].split("=")[-1]) )
                page_amount = int(soup.select('.pages')[0].select("a")[-1].attrs['href'].split("=")[-1])
        return page_amount

    @staticmethod
    def get_page_prods(in_url, products):
        res = requests.get(in_url)  ### request 的 get 去向 server 提出get 來抓取 html
        res.encoding = "utf8"       ### request 下來的html 要怎麼 encode
        soup = BeautifulSoup(res.text, "lxml") ### parse request下來的html， 第二個參數是選擇parser，然後要記得 pip install lxml 喔！
        
        # prods = []
        for prod in soup.select("#SIL_block"):
            for detail in prod.select("#SIL_item"):
                details = {}
                details["prod_title"] = detail.select('span')[2].text
                #details.append(detail.select('a')[1].select('span')[0].text)
                details["price"]    = detail.select('.red')[1].select('span')[2].text
                details["prod_url"] = detail.select('a')[0].attrs['href']
                details["img_url"]  =detail.select('img')[0].attrs['src']
                details["shop_id"]  = detail.select('a')[2].text

                products.add_prod( **details )
                # prods.append( Product(details[0], details[1], details[2], details[3]) )
        # return prods

    @staticmethod
    def get_prods_image(products, dst_dir, start_index=0,main_log=None, prod_title=False):
        from urllib.request import urlopen
        for go_prod, prod in enumerate(products.prods[start_index:]):
            ### 流水號 + prod_title，再找 wants 的 關鍵字 較方便
            if(prod_title): 
                Check_dir_exist_and_build(dst_dir + "/have_title")
                img_name = "have_title/%04i_"%(go_prod+1) + f"{ Scraper_util.filte_invalid_symbol( prod.prod_title ) }.jpg"
                ### 怕產品名稱太長！
                if(len(img_name) > 200):
                    img_name = "have_title/%04i_"%(go_prod+1) + f"{ Scraper_util.filte_invalid_symbol( prod.prod_title[:100] ) }.jpg" 

            ### 純 流水號，寫word時覺得還是用這個好了，word在讀圖的時候比較方便
            else:  
                img_name = f"%04i.jpg"%(go_prod+1)
            img_path = dst_dir + "/" + img_name
            img_byte = urlopen(prod.img_url)
            with open( img_path, "wb") as f:
                print("download to " + img_path )
                f.write(img_byte.read())
            if( (go_prod+1) %50==0 ): time.sleep(3) ### 怕抓太快被擋
