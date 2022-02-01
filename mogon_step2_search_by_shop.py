import time
import sys 
# sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from kong_util.build_dataset_combine import Check_dir_exist_and_build, Check_dir_exist_and_build_new_dir

from RW_util import RW_to_file
from mogon_step1_scraper import PLATFORM, MogonSearch_obj

class Shop(MogonSearch_obj):
    def __init__(self):
        self.platform = None  ### 基本
        self.shop_name = None   ### 基本
        self.shop_url = None  ### 由上兩個基本來設定

        self.prods_dir = None ### 設定 shop的prods_dir放哪裡

    def _init_search_obj(self, base_url, prods_dir): ### 初始化 search_obj ( 建立products物件)
        super().__init__(base_url=base_url, prods_dir=prods_dir)

class Shop_builder:
    def __init__(self, shop=None):
        if(shop is None): self.shop = Shop()
        else: self.shop = shop 

    def _set_and_build_shop_dir(self):
        ### 設定url
        url = f"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action={self.shop.platform.value}&"
        if  (self.shop.platform == PLATFORM.jraku): url += f"shopCode={self.shop.shop_name}"
        elif(self.shop.platform == PLATFORM.yahooshop):   url += f"store={self.shop.shop_name}"
        elif(self.shop.platform == PLATFORM.yahoobid):        url += f"seller={self.shop.shop_name}"
        self.shop.shop_url = url

        ### 設定目的地資料夾
        self.shop.prods_dir = f"shop_search/{self.shop.shop_name}/{self.shop.platform.value}"

        ### 建立products物件
        self.shop._init_search_obj(base_url=self.shop.shop_url, prods_dir=self.shop.prods_dir)

    def build(self, platform, shop_name):
        self.shop.platform = platform
        self.shop.shop_name = shop_name
        self._set_and_build_shop_dir()
        return self.shop 

class Shop_product_filter:
    @staticmethod
    def filter_title(shop, wants=[]):
        new_prods = []
        for prod in shop.products.prods:
            for want in wants:
                if(want in prod.prod_title ):
                    new_prods.append(prod)
        shop.products.prods = new_prods

###############################################################################
### 建立shop物件
shop_kurosa       = Shop_builder().build( PLATFORM.jraku, "kurosawahonten") ### 建立 shop_kurosa，但爬下來沒有且不像樂器店
# shop_rizing       = Shop_builder().build( PLATFORM.yahooshop, "rizing") ### 建立 rizing ### 好像全部都是
# shop_auc_rizing   = Shop_builder().build( PLATFORM.jraku, "auc-rizing") ### 建立 auc-rizing
# shop_merry_net    = Shop_builder().build( PLATFORM.jraku, "merry-net") ### 建立 merry-net
# shop_soarsound    = Shop_builder().build( PLATFORM.jraku, "soarsound") ### 建立 soarsound ### 有m3001
# shop_mikidj       = Shop_builder().build( PLATFORM.jraku, "mikidj") ### 建立 mikidj ### 有m3001
# shop_deeplearning = Shop_builder().build( PLATFORM.jraku, "deeplearning") ### 建立 deeplearning ### 有m3001，但爬下來沒有且不像樂器店

if(__name__=="__main__"):
    ### 看看各個 shop的 產品價錢 和 產品名稱，可以從這裡看 wants使用的title
    # shop_kurosa      .use_b_download_prods_img(price=True, prod_title=True )
    # shop_rizing      .use_b_download_prods_img(price=True, prod_title=True )
    # shop_deeplearning.use_b_download_prods_img(price=True, prod_title=True )
    # shop_mikidj      .use_b_download_prods_img(price=True, prod_title=True )
    # shop_soarsound   .use_b_download_prods_img(price=True, prod_title=True )
    # shop_merry_net   .use_b_download_prods_img(price=True, prod_title=True )
    # shop_auc_rizing  .use_b_download_prods_img(price=True, prod_title=True )

    ### 寫入docx
    # shop_kurosa.use_c_write_to_word(restart_url=True)                     ### prods.txt 和 prods_img 都重新下載，再寫 docx
    # shop_kurosa.use_c_write_to_word(restart_url=False, restart_img=True)  ### 用現存的prods.txt，重新下載 prods_img，再寫 docx
    # shop_kurosa.use_c_write_to_word(restart_url=False, restart_img=False) ### 如果 prods.txt 和 prods_img 都已經確定好對應了，直接寫docx

    ########################################################################################################################################################
    ########################################################################################################################################################
    ### 一些拆開寫的例子

    ### 取得 shop內所有頁面的products
    # shop_kurosa.get_all_page_prods() 

    ##################################################################################
    ### 用 prods 來 抓圖片
    # shop_kurosa.get_all_page_prods_img()

    ##################################################################################
    ### 要有 文字 和 圖片 才能寫進word裡
    ### 這部分的參數要用 絕對位置喔！
    # RW_to_file.write_MogonSearch_to_word(shop_kurosa)

    ##################################################################################
    # RW_to_file.write_MogonSearch_obj(shop_kurosa) ### 把 shop.prods 存入檔案
    # print(shop_kurosa)  ### 看一下取得如何

    ##################################################################################
    ### 如果已經抓過且有存起來不想花時間重新抓，用這裡的讀取上次存的結果
    # RW_to_file.read_MogonSearch_obj(shop_kurosa) ### 取得 之前存的 shop.prods 檔案
    # print(shop_kurosa)  ### 看一下取得如何

    ##################################################################################
    ### filter 產品名稱
    # Shop_product_filter.filter_title(shop_kurosa, wants=["新品", "NEWS", "輸入盤", "【送料無料】"])
    # print(shop_kurosa)


    ########################################################################################################################################################
    ### 以shop搜尋 的時候 網址大概的長相
    ### "http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jyahooshopping&store=rizing&page=" #40
    ### "http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jrakutenshopping&shopCode=liberty-it&page=" #100
    ### "http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jyahooshopping&store=merry-net&page=" #40
    ### "http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jrakutenshopping&shopCode=e-gakkinet&&page=" #100
    ### "http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jyahooshopping&store=gakki-de-genki&page="
    ### "http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jrakutenshopping&shopCode=kurosawahonten&page="
    ### "http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action=jyahooshopping&store=gakki-de-genki&page=40"