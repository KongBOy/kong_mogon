import time
import sys 
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from build_dataset_combine import Check_dir_exist_and_build, Check_dir_exist_and_build_new_dir


from mogon_base_util import Products, Scraper_util, RW_to_file, PLATFORM


class Shop:
    def __init__(self):
        self.platform = None  ### 基本
        self.shop_id = None   ### 基本
        self.shop_url = None  ### 由上兩個基本來設定

        self.prods_dir = None ### 設定 shop的prods_dir放哪裡
        self.products = None  ### 建立 products 物件 (放product的容器 和 記錄一些 來源url/目的地資料夾 的東西)
    
    def get_all_page_prods(self):
        Scraper_util.get_all_page_prods(self.products)

    def get_all_page_prods_img(self, prod_num=True, prod_title=False, shop_id=False):
        Scraper_util.get_all_page_prods_img(self.products, prod_title=prod_title)

    def __str__(self):
        prod_string = ""
        for go_prod, prod in enumerate(self.products.prods): prod_string += f"%04i {prod.prod_title}\n"%go_prod
        return prod_string
        

class Shop_builder:
    def __init__(self, shop=None):
        if(shop is None): self.shop = Shop()
        else: self.shop = shop 

    def _set_and_build_shop_dir(self):
        ### 設定url
        url = f"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action={self.shop.platform.value}&"
        if  (self.shop.platform == PLATFORM.jraku): url += f"shopCode={self.shop.shop_id}"
        elif(self.shop.platform == PLATFORM.yahooshop):   url += f"store={self.shop.shop_id}"
        elif(self.shop.platform == PLATFORM.yahoobid):        url += f"seller={self.shop.shop_id}"
        self.shop.shop_url = url

        ### 設定目的地資料夾
        self.shop.prods_dir = f"{self.shop.shop_id}/{self.shop.platform.value}"

        ### 建立products物件
        self.shop.products = Products(base_url=self.shop.shop_url, prods_dir=self.shop.prods_dir)

    def build(self, platform, shop_id):
        self.shop.platform = platform
        self.shop.shop_id = shop_id
        self._set_and_build_shop_dir()
        return self.shop 



class Shop_product_filter:
    @staticmethod
    def filter_prods(shop, wants=[]):
        new_prods = []
        for prod in shop.products.prods:
            for want in wants:
                if(want in prod.prod_title ):
                    new_prods.append(prod)
        shop.products.prods = new_prods






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
shop_kurosa       = Shop_builder().build( PLATFORM.jraku, "kurosawahonten") ### 建立 shop_kurosa，但爬下來沒有且不像樂器店
# shop_rizing       = Shop_builder().build( PLATFORM.yahooshop, "rizing") ### 建立 rizing ### 好像全部都是
# shop_auc_rizing   = Shop_builder().build( PLATFORM.jraku, "auc-rizing") ### 建立 auc-rizing
# shop_merry_net    = Shop_builder().build( PLATFORM.jraku, "merry-net") ### 建立 merry-net
# shop_soarsound    = Shop_builder().build( PLATFORM.jraku, "soarsound") ### 建立 soarsound ### 有m3001
# shop_mikidj       = Shop_builder().build( PLATFORM.jraku, "mikidj") ### 建立 mikidj ### 有m3001
# shop_deeplearning = Shop_builder().build( PLATFORM.jraku, "deeplearning") ### 建立 deeplearning ### 有m3001，但爬下來沒有且不像樂器店

step0_see_wants_title(shop_kurosa)
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