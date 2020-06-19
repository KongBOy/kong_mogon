from mogon_base_util import Products, Scraper_util, PLATFORM, RW_to_file

class Keyword:
    def __init__(self):
        self.platform = None     ### 基本
        self.keyword = None      ### 基本
        self.keyword_url = None  ### 由上兩個基本來設定

        self.prods_dir = None    ### 設定 Keyword的prods_dir放哪裡
        self.products = None     ### 建立 products物件 (放product的容器 和 記錄一些 來源url/目的地資料夾 的東西)

    def __str__(self):
        prod_string = ""
        for go_prod, prod in enumerate(self.products.prods): prod_string += f"%04i {prod.prod_title}\n"%go_prod
        return prod_string


    ### 分成 get_all_page_prods 和 
    ###      get_all_page_prods_imgs 兩階段是因為：如果再抓多頁面時，經常被擋，如果寫在一起，就要一起全部重新開始，所以才分成兩階段喔！
    def get_all_page_prods(self):
        Scraper_util.get_all_page_prods(self.products)

    def get_all_page_prods_img(self, prod_num=True, prod_title=False, shop_id=False):
        Scraper_util.get_all_page_prods_img(self.products, prod_num, prod_title, shop_id)



class Keyword_builder:
    def __init__(self, keyword=None):
        if(keyword is None): self.keyword_obj = Keyword()
        else: self.keyword_obj = keyword 

    def _set_and_build_dir(self):
        ### 設定url
        url = f"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action={self.keyword_obj.platform.value}&keyword={self.keyword_obj.keyword}&SearchMethod=multi"
        self.keyword_obj.keyword_url = url

        ### 設定目的地資料夾
        self.keyword_obj.prods_dir = f"{self.keyword_obj.keyword}/{self.keyword_obj.platform.value}"

        ### 建立products物件
        self.keyword_obj.products = Products(base_url=self.keyword_obj.keyword_url, prods_dir=self.keyword_obj.prods_dir)

    def build(self, platform, keyword):
        self.keyword_obj.platform = platform
        self.keyword_obj.keyword = keyword
        self._set_and_build_dir()
        return self.keyword_obj 


key_playwood = Keyword_builder().build( PLATFORM.jraku, "playwood") ### 建立 shop_kurosa，但爬下來沒有且不像樂器店
key_playwood.get_all_page_prods()
RW_to_file.write_shop_prods(key_playwood) ### 把 shop.prods 存入檔案
RW_to_file.read_shop_prods(key_playwood) ### 取得 之前存的 shop.prods 檔案
key_playwood.get_all_page_prods_img(prod_num=False, prod_title=True, shop_id=True)

key_playwood = Keyword_builder().build( PLATFORM.yahoobid, "playwood") ### 建立 shop_kurosa，但爬下來沒有且不像樂器店
key_playwood.get_all_page_prods()
RW_to_file.write_shop_prods(key_playwood) ### 把 shop.prods 存入檔案
RW_to_file.read_shop_prods(key_playwood) ### 取得 之前存的 shop.prods 檔案
key_playwood.get_all_page_prods_img(prod_num=False, prod_title=True, shop_id=True)

key_playwood = Keyword_builder().build( PLATFORM.yahooshop, "playwood") ### 建立 shop_kurosa，但爬下來沒有且不像樂器店
key_playwood.get_all_page_prods()
RW_to_file.write_shop_prods(key_playwood) ### 把 shop.prods 存入檔案
RW_to_file.read_shop_prods(key_playwood) ### 取得 之前存的 shop.prods 檔案
key_playwood.get_all_page_prods_img(prod_num=False, prod_title=True, shop_id=True)


