import requests
from bs4 import BeautifulSoup
import time

import sys 
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from build_dataset_combine import Check_dir_exist_and_build, Check_dir_exist_and_build_new_dir
from util import get_dir_certain_file_name

from abc import abstractmethod

from enum import Enum, auto
class PLATFORM(Enum):
    jraku = "jrakutenshopping"
    yahoobid = "jyahoobid"
    yahooshop = "jyahooshopping"
plat_jraku = PLATFORM.jraku 
plat_yahoobid = PLATFORM.yahoobid 
plat_yahooshop = PLATFORM.yahooshop 



class Product:
    def __init__(self, prod_title, price, prod_url, img_url, shop_name):
        self.prod_title = prod_title
        self.price = price
        self.prod_url = prod_url
        self.img_url = img_url
        self.shop_name = shop_name

    def __str__(self):
        return "\n".join([self.prod_title, self.price, self.prod_url, self.img_url, self.shop_name])


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
    
    def add_prod(self, prod_title, price, prod_url, img_url, shop_name):
        self.prods.append( Product(prod_title, price, prod_url, img_url, shop_name) )

    def read_prods_from_file(self, path):
        with open( path , "r" , encoding = "utf8") as f:
            details = {}
            for go_line, line in enumerate(f):
                if  ( (go_line+1)% 5 == 1 ): details["prod_title"] = line.rstrip("\n")
                elif( (go_line+1)% 5 == 2 ): details["price"]      = line.rstrip("\n")
                elif( (go_line+1)% 5 == 3 ): details["prod_url"]   = line.rstrip("\n")
                elif( (go_line+1)% 5 == 4 ): details["img_url"]   = line.rstrip("\n")
                elif( (go_line+1)% 5 == 0 ): details["shop_name"]   = line.rstrip("\n")

                if( (go_line+1)% 5 == 0 ):
                    self.add_prod( **details )
                    del details
                    details = {}

#############################################################################################################################################
#############################################################################################################################################
class Search_obj:
    def __init__(self, base_url, prods_dir):
        self.products = Products(base_url=base_url, prods_dir=prods_dir)

    def __str__(self):
        prod_string = ""
        for go_prod, prod in enumerate(self.products.prods): prod_string += f"%04i {prod.prod_title}\n"%go_prod
        return prod_string

    #############################################################################################################################################
    ### 分成 get_all_page_prods 和 
    ###      get_all_page_prods_imgs 兩階段是因為：如果再抓多頁面時，經常被擋，如果寫在一起，就要一起全部重新開始，所以才分成兩階段喔！
    def get_all_page_prods(self):
        Scraper_util.get_all_page_prods(self.products)

    def get_all_page_prods_img(self, prod_num=True, prod_title=False, shop_name=False, price=False):
        Scraper_util.get_all_page_prods_img(self.products, prod_num=prod_num, prod_title=prod_title, shop_name=shop_name, price=price)

    #############################################################################################################################################
    def sort_by_key(self, sort_key):
        if(sort_key == "shop_name" ): self.products.prods = sorted(self.products.prods, key=lambda prod:prod.shop_name)
        if(sort_key == "price"     ): self.products.prods = sorted(self.products.prods, key=lambda prod:prod.price)
        if(sort_key == "prod_title"): self.products.prods = sorted(self.products.prods, key=lambda prod:prod.prod_title)

    #############################################################################################################################################
    def _check_prods_in_ram_or_file(self, sort_key=None):
        import os
        if(len(self.products.prods)==0): ### 如果 現在products是空的 且 之前有存檔過prods.txt 才去抓資料喔， products不是空的在抓資料 這可能是自己操作失誤，從網路抓 又從 檔案讀，總共抓了兩次 ，下載的img就重複了喔！
            print("目前 RAM 內沒有 products 資料")
            if(os.path.isfile(self.products.prods_dir+"/prods.txt")): ### 先看看有沒有上次的紀錄，沒有再從網路上重新抓
                print("有上次的products資料，讀取上次的資料")
                RW_to_file.read_prods_to_search_obj(self) ### 取得 之前存的 search_obj 抓到的 prods檔案
                self.sort_by_key( sort_key )
            else: ### 沒有上次的紀錄，從網路上重新抓，順便存起來
                print("沒有products資料檔，重新從網路抓資料")
                self.get_all_page_prods()
                self.sort_by_key( sort_key )
                RW_to_file.write_prods_from_search_obj(self)

    def _check_imgs_downloaded(self, sort_key=None):
        file_name = get_dir_certain_file_name(self.products.prods_img_dir, ".jpg")
        if( len(file_name) == 0 ): ### 如果 prods_imgs資料夾下面是空的，用use_b去下載imgs
            print("圖片還沒有下載，現在自動去下載 RAM內products 的 imgs 囉！")
            self.sort_by_key( sort_key )
            self.use_b_download_prods_img()
        print("products 和 imgs 都存在")


    #############################################################################################################################################
    def use_a_download_prods_and_write_file(self, restart_url=False, sort_key=None):
        if  (restart_url == True) : 
            self.get_all_page_prods()  ### 直接從 網路上抓products
            self.sort_by_key( sort_key )
            RW_to_file.write_prods_from_search_obj(self) ### 把 search_obj 抓到的 prods 存入檔案
        elif(restart_url == False): self._check_prods_in_ram_or_file() ### 先看看之前的prods紀錄，有的話讀取之前的prods，沒有的話重新從網路上抓prods並存入檔案
        

    def use_b_download_prods_img(self,restart_url=False, prod_num=True, shop_name=False, price=False, prod_title=False, sort_key=None):
        if(restart_url == True): ### 直接重新抓prods
            self.use_a_download_prods_and_write_file(restart_url=True, sort_key=sort_key) ### 直接從 網路上抓products 並 存入檔案
        elif(restart_url == False): ### 先看看之前的prods紀錄，有的話讀取之前的prods來抓prods_img，沒有的話重新從網路上抓prods並存入檔案
            self.use_a_download_prods_and_write_file(restart_url=False, sort_key=sort_key)  ### 先看看以前 有沒有存過 prods.txt，有的話就用之前的prods.txt紀錄，沒有的話 重新從網路上抓 並存入檔案
        self.get_all_page_prods_img( prod_num=prod_num, prod_title=prod_title, shop_name=shop_name, price=price) ### 抓prods_img
            

    def use_c_write_to_word(self, restart_url=False, restart_img=False, sort_key=None):
        if(restart_url==True): ### 直接重新抓prods 和 prods_img
            self.use_b_download_prods_img(restart_url=True, sort_key=sort_key)
        elif(restart_url == False):
            ###請注意，這裡的 _check 沒有保證 prods.txt 和 prods_img 有對應喔！如果想對應要再多寫function，或用下面的elif
            if  (restart_img == True): ### 根據 prods 重新下載 prods_img！但是如果有3000張影像，每次要重新下載很麻煩，如果之前已下載過 且 事前已經確認 prods_img 和 prods.txt 是對應的，可以用elif直接寫docx
                self.use_b_download_prods_img(restart_url=False, sort_key=sort_key) 
            elif(restart_img == False): ### 如果存在 prods.txt 和 prods_img，就直接寫docx(但不保證 prods.txt 和 prods_img 對應關係，請事前確認)
                self._check_prods_in_ram_or_file(sort_key=sort_key) ### 先看看之前的prods紀錄，有的話讀取之前的prods來抓prods_img，沒有的話重新從網路上抓prods並存入檔案
                self._check_imgs_downloaded(sort_key=sort_key)      ### 先看看之前的prods_img資料夾是不是空的，空的話就重新下載，非空不做事，也要注意一下不保證存在的imgs 和 目前的 prods 是有對影的喔，用前請先自行確認一定對應
        RW_to_file.write_prods_from_search_obj_to_word(self) ### 寫docx


#############################################################################################################################################
#############################################################################################################################################
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
                
                if(len(detail.select('a')) >= 3 ) :details["shop_name"]  = detail.select('a')[2].text ### 正常<a>應該有4個，且店家會在第3個<a>
                else:                              details["shop_name"]  = detail.select('a')[0].text ### 違禁品<a>只有兩個，且店家會在第1個<a>
                # print("a_amount", len(detail.select('a')), details["shop_name"])
                products.add_prod( **details )
    
    
    @staticmethod
    def get_all_page_prods( products):
        page_amount = Scraper_util.get_page_amount(products.base_url) ### 取得 頁數
        print("page_amount:",page_amount)
        # page_amount = 2 ### debug用
        for go_page in range(page_amount): ### 走訪每一頁，把products撈出來
            full_url = products.base_url +"&page="+ str(go_page+1) ### page是從1開始
            Scraper_util.get_page_prods( full_url, products ) ### 把 容器 丟進去function內 渲染

            print(full_url + " read ok!!!!")
            with open(products.prods_dir +"/main_log.txt","a") as main_log: main_log.write(full_url + " read ok!!!! \n")
            if( (go_page+1)%10 ==0): time.sleep(8) ### 怕抓太快被擋，抓10頁休息5秒

    ##########################################################################################################################################
    @staticmethod
    def _get_prods_image(products, start_index=0,main_log=None, prod_num=True, shop_name=False, price=False, prod_title=False):
        from urllib.request import urlopen
        for go_prod, prod in enumerate(products.prods[start_index:]):
            ### 去網路上 抓影像囉！
            img_byte = urlopen(prod.img_url)   

            ### 決定要存哪裡
            ### 1.決定img_name
            img_name = ""
            if(prod_num): img_name = "%04i"%(go_prod+1)  ### 最基本純流水號
            if(shop_name or prod_title or prod_title):   
                if(shop_name):    img_name += f"_{ prod.shop_name }"       ### 加shop_name
                if(price):      img_name += f"_{ prod.price }"
                if(prod_title): img_name += f"_{ prod.prod_title }"    ### 加prod_title
                if(len(img_name) > 120): img_name =  img_name[:120]    ### 怕img_name太長！
                img_name = Scraper_util.filte_invalid_symbol( img_name )  ### 去除 不能命名的符號
            if(img_name == ""): img_name = "%04i"%(go_prod+1) ### 防呆，以避免 prod_num, prod_num, shop_name 全為 False
            img_name += ".jpg"  

            ### 2.決定img_sub_dir
            img_sub_dir = ""
            if(shop_name or prod_title or prod_title):
                img_sub_dir += "have"
                if(prod_num):   img_sub_dir += "-num"       ### 加shop_name
                if(shop_name):    img_sub_dir += "-shop_name"       ### 加shop_name
                if(price):      img_sub_dir += "-price"
                if(prod_title): img_sub_dir += "-title"    ### 加prod_title
            Check_dir_exist_and_build(products.prods_img_dir + "/" + img_sub_dir)

            ### 3.根據 img_name 和 img_sub_dir 設定 img_path
            img_path = products.prods_img_dir + "/" + img_sub_dir + "/" + img_name

            ### 4.把 圖片根據 img_path 存起來
            with open( img_path, "wb") as f:
                print(f"{go_prod}/{len(products.prods[start_index:])} download to " + img_path )
                f.write(img_byte.read())

            ### 怕抓太快被擋
            if( (go_prod+1) %50==0 ): time.sleep(8) 

    @staticmethod
    def get_all_page_prods_img( products, prod_num=True, prod_title=False, shop_name=False, price=False):
        if(products.prods == []) : Scraper_util.get_all_page_prods(products) ### 如果 prods是空的，就先去抓 prods囉！
        Scraper_util._get_prods_image(products, start_index=0, prod_num=prod_num, prod_title=prod_title, shop_name=shop_name, price=price)


class RW_to_file:
    @staticmethod
    def write_prods_from_search_obj(search_obj):
        with open( search_obj.prods_dir+"/prods.txt" , "w" , encoding = "utf8") as f:
            for go_prod, prod in enumerate(search_obj.products.prods):
                f.write(str(prod))
                if(go_prod != len(search_obj.products.prods)-1): f.write("\n") ### 除了最後一個product外都要換行


    @staticmethod
    def read_prods_to_search_obj(search_obj):
        search_obj.products.read_prods_from_file( path=search_obj.prods_dir+"/prods.txt" ) 


    @staticmethod
    def write_prods_from_search_obj_to_word(search_obj):
        import os
        from win32com import client
        ### word的操作全部都要是 絕對路徑喔！
        cur_path = os.getcwd()

        word = client.gencache.EnsureDispatch('word.application')
        word.Visible = 1
        word.DisplayAlerts = 0
        doc = word.Documents.Add()

        range1 = doc.Range(0,0)

        grid_row_amount = len(search_obj.products.prods) + 1 ### +1 for title
        grid_col_amount = 4

        table = doc.Tables.Add(range1, grid_row_amount, grid_col_amount)
        table.Cell(1,1).Range.InsertAfter("Product_name")
        table.Cell(1,2).Range.InsertAfter("Product_price")
        table.Cell(1,3).Range.InsertAfter("Product_link")
        table.Cell(1,4).Range.InsertAfter("Product_image")

        for go_prod, prod in enumerate(search_obj.products.prods):
            table.Cell( 2+go_prod, 1 ).Range.InsertAfter(prod.prod_title)
            table.Cell( 2+go_prod, 2 ).Range.InsertAfter(prod.price)
            table.Cell( 2+go_prod, 3 ).Range.InsertAfter(prod.prod_url)
            # print(search_obj.prods_img_dir+"/"+"%04i.jpg"%(go_prod+1))
            table.Cell( 2+go_prod, 4 ).Range.InlineShapes.AddPicture(cur_path + "/" + search_obj.products.prods_img_dir + "/"+"%04i.jpg"%(go_prod+1),False,True)
            print("docx row:%04i finished~~"%go_prod)
        doc.SaveAs( cur_path + "/" + search_obj.products.prods_dir + "/products.docx")
        doc.Close()
        #word.Quit()