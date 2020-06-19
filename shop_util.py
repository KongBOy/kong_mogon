import time
import sys 
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from build_dataset_combine import Check_dir_exist_and_build, Check_dir_exist_and_build_new_dir
from enum import Enum, auto

from mogon_base_util import Products,Scraper_util

class Shop:
    def __init__(self):
        self.platform = None
        self.shop_id = None
        self.shop_url = None

        self.prods_dir = None      ### shop/platform
        self.prods_img_dir = None  ### shop/platform/imgs
        self.doc_dir = None        ### shop/platform

        self.products = Products()
        # self.imgs = []
        # self.doc = None

    
    ### 分成 get_all_page_prods 和 
    ###      get_all_page_prods_img 兩階段是因為：如果再抓多頁面時，經常被擋，如果寫在一起，就要一起全部重新開始，所以才分成兩階段喔！
    def get_all_page_prods(self):
        page_amount = Scraper_util.get_page_amount(self.shop_url)
        print("page_amount:",page_amount)
        page_amount = 2 ### debug用
        for go_page in range(page_amount):
            full_url = self.shop_url +"&page="+ str(go_page+1) ### page是從1開始
            Scraper_util.get_page_prods( full_url, self.products )

            print(full_url + " read ok!!!!")
            with open(self.prods_dir +"/main_log.txt","a") as main_log: main_log.write(full_url + " read ok!!!! \n")
            if( (go_page+1)%10 ==0): time.sleep(5) ### 怕抓太快被擋，抓10頁休息5秒

    def get_all_page_prods_img(self, prod_title=False):
        if(self.products.prods == []) : self.get_all_page_prods() ### 如果 prods是空的，就先去抓 prods囉！
        Scraper_util.get_prods_image(self.products, self.prods_img_dir, start_index=0, prod_title=prod_title)

    def __str__(self):
        prod_string = ""
        for go_prod, prod in enumerate(self.products.prods): prod_string += f"%04i {prod.prod_title}\n"%go_prod
        return prod_string
        


class Shop_builder:
    def __init__(self, shop=None):
        if(shop is None): self.shop = Shop()
        else: self.shop = shop 

    def _set_and_build_shop_dir(self):
        url = f"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action={self.shop.platform.value}&"
        if  (self.shop.platform == PLATFORM.jrakutenshopping): url += f"shopCode={self.shop.shop_id}"
        elif(self.shop.platform == PLATFORM.jyahooshopping):   url += f"store={self.shop.shop_id}"
        elif(self.shop.platform == PLATFORM.jyahoobid):        url += f"seller={self.shop.shop_id}"
        self.shop.shop_url = url

        self.shop.prods_dir = f"{self.shop.shop_id}/{self.shop.platform.value}"
        self.shop.doc_dir   = self.shop.prods_dir 
        self.shop.prods_img_dir  = f"{self.shop.shop_id}/{self.shop.platform.value}/imgs"
        Check_dir_exist_and_build(self.shop.prods_dir)
        Check_dir_exist_and_build(self.shop.doc_dir)
        Check_dir_exist_and_build(self.shop.prods_img_dir)

    def build(self, platform, shop_id):
        self.shop.platform = platform
        self.shop.shop_id = shop_id
        self._set_and_build_shop_dir()
        return self.shop 




class RW_to_file:
    @staticmethod
    def write_shop_prods(shop):
        with open( shop.prods_dir+"/prods.txt" , "w" , encoding = "utf8") as f:
            for go_prod, prod in enumerate(shop.products.prods):
                f.write(str(prod))
                if(go_prod != len(shop.products.prods)-1): f.write("\n") ### 除了最後一個product外都要換行

    @staticmethod
    def read_shop_prods(shop):
        print(shop.prods_dir+"/prods.txt")
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


class Shop_product_filter:
    @staticmethod
    def filter_prods(shop, wants=[]):
        new_prods = []
        for prod in shop.products.prods:
            for want in wants:
                if(want in prod.prod_title ):
                    new_prods.append(prod)
        shop.products.prods = new_prods



class PLATFORM(Enum):
    jrakutenshopping = "jrakutenshopping"
    jyahooshopping = "jyahooshopping"
    jyahoobid = "jyahoobid"
plat_jraku = PLATFORM.jrakutenshopping 
plat_yahoobid = PLATFORM.jyahoobid 
plat_yahooshop = PLATFORM.jyahooshopping 



def step0_see_wants_title(shop):
    shop.get_all_page_prods() 
    RW_to_file.write_shop_prods(shop) ### 把 shop.prods 存入檔案
    RW_to_file.read_shop_prods(shop) ### 取得 之前存的 shop.prods 檔案
    shop.get_all_page_prods_img(prod_title=True)

def step_write_to_word(shop):
    shop.get_all_page_prods_img(prod_title=False)
    RW_to_file.write_shop_prods(shop) ### 把 shop.prods 存入檔案
    RW_to_file.write_shop_prods_to_word(shop)

def step1_grab_prods_from_web(shop):
    shop.get_all_page_prods() 
    RW_to_file.write_shop_prods(shop) ### 把 shop.prods 存入檔案

def step2_grab_prods_img_from_web_see_title(shop):
    shop.prods = RW_to_file.read_shop_prods(shop) ### 取得 之前存的 shop.prods 檔案
    shop.get_all_page_prods_img(prod_title=True)
###############################################################################
### 建立shop物件
shop_kurosa       = Shop_builder().build( plat_jraku, "kurosawahonten") ### 建立 shop_kurosa，但爬下來沒有且不像樂器店
# shop_rizing       = Shop_builder().build( plat_yahooshop, "rizing") ### 建立 rizing ### 好像全部都是
# shop_auc_rizing   = Shop_builder().build( plat_jraku, "auc-rizing") ### 建立 auc-rizing
# shop_merry_net    = Shop_builder().build( plat_jraku, "merry-net") ### 建立 merry-net
# shop_soarsound    = Shop_builder().build( plat_jraku, "soarsound") ### 建立 soarsound ### 有m3001
# shop_mikidj       = Shop_builder().build( plat_jraku, "mikidj") ### 建立 mikidj ### 有m3001
# shop_deeplearning = Shop_builder().build( plat_jraku, "deeplearning") ### 建立 deeplearning ### 有m3001，但爬下來沒有且不像樂器店

step_write_to_word(shop_kurosa)
# step0_see_wants_title(shop_kurosa)
# step0_see_wants_title(shop_rizing)
# step0_see_wants_title(shop_deeplearning)
# step0_see_wants_title(shop_mikidj)
# step0_see_wants_title(shop_soarsound)
# step0_see_wants_title(shop_merry_net)
# step0_see_wants_title(shop_auc_rizing)
###############################################################################
### 取得 shop內所有頁面的products
# shop_kurosa.get_all_page_prods() 

########################################################################################################################################################
### 用 prods 來 抓圖片
# shop_kurosa.get_all_page_prods_img()

########################################################################################################################################################
### 要有 文字 和 圖片 才能寫進word裡
### 這部分的參數要用 絕對位置喔！
# RW_to_file.write_shop_prods_to_word(shop_kurosa)

###############################################################################
# RW_to_file.write_shop_prods(shop_kurosa) ### 把 shop.prods 存入檔案
# print(shop_kurosa)  ### 看一下取得如何

###############################################################################
### 如果已經抓過且有存起來不想花時間重新抓，用這裡的讀取上次存的結果
# shop_kurosa.prods = RW_to_file.read_shop_prods(shop_kurosa) ### 取得 之前存的 shop.prods 檔案
# print(shop_kurosa)  ### 看一下取得如何

###############################################################################
# print(shop_kurosa)
# Shop_product_filter.filter_prods(shop_kurosa, wants=["新品", "NEWS", "輸入盤", "【送料無料】"])
# print(shop_kurosa)


########################################################################################################################################################
###"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jyahooshopping&store=rizing&page=" #40
###"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jrakutenshopping&shopCode=liberty-it&page=" #100
###"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jyahooshopping&store=merry-net&page=" #40
###"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jrakutenshopping&shopCode=e-gakkinet&&page=" #100
###"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jyahooshopping&store=gakki-de-genki&page="
###"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jrakutenshopping&shopCode=kurosawahonten&page="
###"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jyahooshopping&store=gakki-de-genki&page=40"