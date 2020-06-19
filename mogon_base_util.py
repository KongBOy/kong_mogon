import requests
from bs4 import BeautifulSoup
import time

import sys 
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from build_dataset_combine import Check_dir_exist_and_build, Check_dir_exist_and_build_new_dir

from abc import abstractmethod

from enum import Enum, auto
class PLATFORM(Enum):
    jraku = "jrakutenshopping"
    yahoobid = "jyahooshopping"
    yahooshop = "jyahoobid"
plat_jraku = PLATFORM.jraku 
plat_yahoobid = PLATFORM.yahoobid 
plat_yahooshop = PLATFORM.yahooshop 



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
    def __init__(self, base_url, prods_dir):
        self.prods = []            ### 建立 容器
        self.base_url = base_url   ### 紀錄 從哪個base_url 來抓 products

        self.prods_dir = prods_dir   ### products 物件放哪裡
        self.prods_img_dir = self.prods_dir+"/imgs"   ### products的imgs 放哪裡
        Check_dir_exist_and_build(self.prods_dir)     ### 建立資料夾
        Check_dir_exist_and_build(self.prods_img_dir) ### 建立資料夾
    
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
                
                if(len(detail.select('a')) >= 3 ) :details["shop_id"]  = detail.select('a')[2].text ### 正常<a>應該有4個，且店家會在第3個<a>
                else:                              details["shop_id"]  = detail.select('a')[0].text ### 違禁品<a>只有兩個，且店家會在第1個<a>
                # print("a_amount", len(detail.select('a')), details["shop_id"])
                products.add_prod( **details )
    
    
    @staticmethod
    def get_all_page_prods( products):
        page_amount = Scraper_util.get_page_amount(products.base_url)
        print("page_amount:",page_amount)
        # page_amount = 2 ### debug用
        for go_page in range(page_amount):
            full_url = products.base_url +"&page="+ str(go_page+1) ### page是從1開始
            Scraper_util.get_page_prods( full_url, products ) ### 把 容器 丟進去function內 渲染

            print(full_url + " read ok!!!!")
            with open(products.prods_dir +"/main_log.txt","a") as main_log: main_log.write(full_url + " read ok!!!! \n")
            if( (go_page+1)%10 ==0): time.sleep(8) ### 怕抓太快被擋，抓10頁休息5秒

    ##########################################################################################################################################
    @staticmethod
    def _get_prods_image(products, start_index=0,main_log=None, prod_num=True, prod_title=False, shop_id=False):
        from urllib.request import urlopen
        for go_prod, prod in enumerate(products.prods[start_index:]):
            img_name = ""
            if(prod_num): img_name = "%04i"%(go_prod+1)  ### 最基本純流水號
            if(prod_title or shop_id):   
                Check_dir_exist_and_build(products.prods_dir + "/have_title") ### 建立資料夾
                if(shop_id):    img_name += f"_{ prod.shop_id }"       ### 加shop_id
                if(prod_title): img_name += f"_{ prod.prod_title }"    ### 加prod_title
                if(len(img_name) > 200): img_name =  img_name[:200]    ### 怕img_name太長！
                img_name = Scraper_util.filte_invalid_symbol( img_name )  ### 去除 不能命名的符號
                img_name = f"have_title/{img_name}.jpg" ### 資料夾 "have_title/"" 要最後加喔！要不然 "/" 會被 filte_invalid_symbol 去掉ˊ口ˋ
            if(img_name == ""): img_name = "%04i.jpg"%(go_prod+1) ### 防呆，以避免 prod_num, prod_num, shop_id 全為 False
            
            img_path = products.prods_dir + "/" + img_name
            img_byte = urlopen(prod.img_url)
            with open( img_path, "wb") as f:
                print("download to " + img_path )
                f.write(img_byte.read())
            if( (go_prod+1) %50==0 ): time.sleep(8) ### 怕抓太快被擋

    @staticmethod
    def get_all_page_prods_img( products, prod_num=True, prod_title=False, shop_id=False):
        if(products.prods == []) : Scraper_util.get_all_page_prods(products) ### 如果 prods是空的，就先去抓 prods囉！
        Scraper_util._get_prods_image(products, start_index=0, prod_num=prod_num, prod_title=prod_title, shop_id=shop_id)


class RW_to_file:
    @staticmethod
    def write_shop_prods(shop):
        with open( shop.prods_dir+"/prods.txt" , "w" , encoding = "utf8") as f:
            for go_prod, prod in enumerate(shop.products.prods):
                f.write(str(prod))
                if(go_prod != len(shop.products.prods)-1): f.write("\n") ### 除了最後一個product外都要換行


    @staticmethod
    def read_shop_prods(shop):
        shop.products.read_prods_from_file( path=shop.prods_dir+"/prods.txt" ) 


    @staticmethod
    def write_shop_prods_to_word(shop):
        import os
        from win32com import client
        ### word的操作全部都要是 絕對路徑喔！
        cur_path = os.getcwd()

        word = client.gencache.EnsureDispatch('word.application')
        word.Visible = 1
        word.DisplayAlerts = 0
        doc = word.Documents.Add()

        range1 = doc.Range(0,0)

        grid_row_amount = len(shop.products.prods) + 1 ### +1 for title
        grid_col_amount = 4

        table = doc.Tables.Add(range1, grid_row_amount, grid_col_amount)
        table.Cell(1,1).Range.InsertAfter("Product_name")
        table.Cell(1,2).Range.InsertAfter("Product_price")
        table.Cell(1,3).Range.InsertAfter("Product_link")
        table.Cell(1,4).Range.InsertAfter("Product_image")

        for go_prod, prod in enumerate(shop.products.prods):
            table.Cell( 2+go_prod, 1 ).Range.InsertAfter(prod.prod_title)
            table.Cell( 2+go_prod, 2 ).Range.InsertAfter(prod.price)
            table.Cell( 2+go_prod, 3 ).Range.InsertAfter(prod.prod_url)
            # print(shop.prods_img_dir+"/"+"%04i.jpg"%(go_prod+1))
            table.Cell( 2+go_prod, 4 ).Range.InlineShapes.AddPicture(cur_path + "/" + shop.prods_img_dir + "/"+"%04i.jpg"%(go_prod+1),False,True)
            print("docx row:%04i finished~~"%go_prod)
        doc.SaveAs( cur_path + "/" + shop.doc_dir + "/products.docx")
        doc.Close()
        #word.Quit()
