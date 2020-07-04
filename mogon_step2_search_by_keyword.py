from RW_util import RW_to_file
from mogon_step2_search_base import PLATFORM , MogonSearch_obj

class Keyword(MogonSearch_obj):
    def __init__(self):
        self.platform = None     ### 基本
        self.keyword = None      ### 基本
        self.keyword_url = None  ### 由上兩個基本來設定

        self.result_dir = None    ### 設定 Keyword的prods_dir放哪裡

    def _init_search_obj(self, base_url, result_dir): ### 初始化 search_obj ( 建立products物件 )
        super().__init__(base_url=base_url, result_dir=result_dir)


class Keyword_builder:
    def __init__(self, keyword=None):
        if(keyword is None): self.keyword_obj = Keyword()
        else: self.keyword_obj = keyword 

    def _set_and_build_dir(self):
        ### 設定url
        url = f"http://www.moganshopping.com/zh_tw/public/search/searchitem.php?action={self.keyword_obj.platform.value}&keyword={self.keyword_obj.keyword}&SearchMethod=multi"
        self.keyword_obj.keyword_url = url

        ### 設定目的地資料夾
        self.keyword_obj.result_dir = f"keyword_search/{self.keyword_obj.keyword}/{self.keyword_obj.platform.value}"

        ### 建立products物件
        self.keyword_obj._init_search_obj(base_url=self.keyword_obj.keyword_url, result_dir=self.keyword_obj.result_dir)

    def build(self, platform, keyword):
        self.keyword_obj.platform = platform
        self.keyword_obj.keyword = keyword
        self._set_and_build_dir()
        return self.keyword_obj 

### dummy的寫法還是留著好了，給以後的自己當例子參考要怎麼拆開簡單寫
### example1：走訪3個平台，看看keyword能找到什麼，無腦用法 只能重新開始 爬url存成prods.txt 再 存圖，  
###             如果想讀之前存的結果時， 爬url和存的兩行註解掉才可以， 要不然 總共會有 read的 和 爬下來的 prods 重複的兩份prods喔！
def exp1_visit_3_platform_download_imgs_dummy(keyword):
    key_at_jraku = Keyword_builder().build( PLATFORM.jraku, keyword) ### 建立 keyword物件
    key_at_jraku.get_all_page_elements()                    ### 爬url存成prods.txt
    RW_to_file.write_MogonSearch_obj(key_at_jraku) ### 把 prods 存入檔案
    # RW_to_file.read_MogonSearch_obj(key_at_jraku)    ### 取得 之前存的 prods 檔案 ### 這行註解打開的話，要把前兩行註解掉喔！
    key_at_jraku.get_all_page_prods_img(prod_num=False, prod_title=True, shop_name=True, price=True)

    key_at_yahoobid = Keyword_builder().build( PLATFORM.yahoobid, keyword) ### 建立 keyword物件
    key_at_yahoobid.get_all_page_elements()                    ### 爬url存成prods.txt
    RW_to_file.write_MogonSearch_obj(key_at_yahoobid) ### 把 prods 存入檔案
    # RW_to_file.read_MogonSearch_obj(key_at_yahoobid)    ### 取得 之前存的 prods 檔案 ### 這行註解打開的話，要把前兩行註解掉喔！
    key_at_yahoobid.get_all_page_prods_img(prod_num=False, prod_title=True, shop_name=True, price=True)

    key_at_yahooshop = Keyword_builder().build( PLATFORM.yahooshop, keyword) ### 建立 keyword物件
    key_at_yahooshop.get_all_page_elements()                    ### 爬url存成prods.txt
    RW_to_file.write_MogonSearch_obj(key_at_yahooshop) ### 把 prods 存入檔案
    # RW_to_file.read_MogonSearch_obj(key_at_yahooshop)    ### 取得 之前存的 prods 檔案 ### 這行註解打開的話，要把前兩行註解掉喔！
    key_at_yahooshop.get_all_page_prods_img(prod_num=False, prod_title=True, shop_name=True, price=True)
### exp用法：給 keyword即可
# exp1_visit_3_platform_download_imgs_dummy("playwood")
# exp1_visit_3_platform_download_imgs_dummy("playwood m-")
# exp1_visit_3_platform_download_imgs_dummy("playwood m- RIZING")
# exp1_visit_3_platform_download_imgs_dummy("playwood m RIZING")
# exp1_visit_3_platform_download_imgs_dummy("playwood RIZING")
# exp1_visit_3_platform_download_imgs_dummy("playwood RIZING")

############################################################################################################################################
### example2：走訪3個平台，看看keyword能找到什麼，用一些包好的function，會先看之前有沒有存prods.txt，有就用之前的，沒有重爬
def exp2_visit_3_platform_download_imgs_and_use_before_things(keyword, restart_url=False):
    key_at_jraku = Keyword_builder().build( PLATFORM.jraku, keyword) ### 建立 keyword物件
    key_at_jraku.use_b_download_prods_img(restart_url=restart_url, prod_num=False, prod_title=True, shop_name=True, price=True)

    key_at_yahoobid = Keyword_builder().build( PLATFORM.yahoobid, keyword) ### 建立 keyword物件
    key_at_yahoobid.use_b_download_prods_img(restart_url=restart_url, prod_num=False, prod_title=True, shop_name=True, price=True)

    key_at_yahooshop = Keyword_builder().build( PLATFORM.yahooshop, keyword) ### 建立 keyword物件
    key_at_yahooshop.use_b_download_prods_img(restart_url=restart_url, prod_num=False, prod_title=True, shop_name=True, price=True)
### exp用法：給 keyword即可
# exp2_visit_3_platform_download_imgs_and_use_before_things("playwood")
# exp2_visit_3_platform_download_imgs_and_use_before_things("playwood m-")
# exp2_visit_3_platform_download_imgs_and_use_before_things("playwood m- RIZING")
# exp2_visit_3_platform_download_imgs_and_use_before_things("playwood m RIZING")
# exp2_visit_3_platform_download_imgs_and_use_before_things("playwood RIZING")
# exp2_visit_3_platform_download_imgs_and_use_before_things("playwood RIZING")

### 想重新爬prods.txt，restart_url=True即可
# exp2_visit_3_platform_download_imgs_and_use_before_things("playwood RIZING", restart_url=True)

####################################################################################################################################
### dummy的寫法還是留著好了，給以後的自己當例子參考要怎麼拆開簡單寫
def exp3_write_to_docx_dummy(platform, keyword):
    key_at_yahooshop = Keyword_builder().build( platform, keyword) ### 建立 keyword物件
    key_at_yahooshop.get_all_page_elements()                    ### 爬url存成prods.txt
    RW_to_file.write_MogonSearch_obj(key_at_yahooshop) ### 把 prods 存入檔案
    # RW_to_file.read_MogonSearch_obj(key_at_yahooshop)    ### 取得 之前存的 prods 檔案 ### 這行註解打開的話，要把前兩行註解掉喔！
    key_at_yahooshop.get_all_page_prods_img(prod_num=False, prod_title=True, shop_name=True, price=True)
    RW_to_file.write_MogonSearch_to_word(key_at_yahooshop)
### exp用法： 給 platform 和 keyword即可
# exp3_write_to_docx_dummy( PLATFORM.yahooshop, "playwood RIZING")


####################################################################################################################################
def exp4_write_to_docx_and_use_before_things(platform, keyword, restart_url=False, restart_img=False, sort_key=None):
    key_at_yahooshop = Keyword_builder().build( platform, keyword) ### 建立 keyword物件
    key_at_yahooshop.use_c_write_to_word(restart_url=restart_url, restart_img=restart_img, sort_key=sort_key)
### exp用法： 給 platform 和 keyword即可
#  (restart_url=False, restart_img=False) ### 一開始 prods.txt和prods_img 什麼都沒有的時候 會自動重爬  或者 如果 prods.txt 和 prods_img 都已經確定好對應了，直接寫docx
#  (restart_url=True)                     ### prods.txt 和 prods_img 都重新下載，再寫 docx
#  (restart_url=False, restart_img=True)  ### 用現存的prods.txt，重新下載 prods_img，再寫 docx
### 2020/06/20 最後用這個囉！
# exp4_write_to_docx_and_use_before_things( PLATFORM.yahooshop, "playwood RIZING", restart_url=True, sort_key="prod_title")

def exp5_manually_search_RIZING_mallet():
    m_1000 = Keyword_builder().build(PLATFORM.yahooshop, "playwood M-1001 RIZING")
    m_3000 = Keyword_builder().build(PLATFORM.yahooshop, "playwood M-3000 RIZING")
    m_6011 = Keyword_builder().build(PLATFORM.yahooshop, "playwood M-6011 RIZING")
    m_6021 = Keyword_builder().build(PLATFORM.yahooshop, "playwood M-6021 RIZING")
    m_7001 = Keyword_builder().build(PLATFORM.yahooshop, "playwood M-7001 RIZING")
    m_611 = Keyword_builder().build(PLATFORM.yahooshop, "playwood M-611 RIZING")
    m_2001 = Keyword_builder().build(PLATFORM.yahooshop, "playwood M-2001 RIZING")
    m_4000 = Keyword_builder().build(PLATFORM.yahooshop, "playwood M-4000 RIZING")
    m_5000 = Keyword_builder().build(PLATFORM.yahooshop, "playwood M-5000 RIZING")
    xg_series = Keyword_builder().build(PLATFORM.yahooshop, "playwood xg RIZING")
    b_series = Keyword_builder().build(PLATFORM.yahooshop, "playwood b-1 RIZING")
    xb_series = Keyword_builder().build(PLATFORM.yahooshop, "playwood xb RIZING")
    m_101 = Keyword_builder().build(PLATFORM.yahooshop, "playwood m-101 RIZING")
    m_201 = Keyword_builder().build(PLATFORM.yahooshop, "playwood m-201 RIZING")
    m_301 = Keyword_builder().build(PLATFORM.yahooshop, "playwood m-301 RIZING")
    m_401 = Keyword_builder().build(PLATFORM.yahooshop, "playwood m-401 RIZING")
    m_501 = Keyword_builder().build(PLATFORM.yahooshop, "playwood m-501 RIZING")
    m_801 = Keyword_builder().build(PLATFORM.yahooshop, "playwood m-801 RIZING")
    m_901 = Keyword_builder().build(PLATFORM.yahooshop, "playwood m-901 RIZING")
    two_tone = Keyword_builder().build(PLATFORM.yahooshop, "playwood two-tone RIZING")
    m_01 = Keyword_builder().build(PLATFORM.yahooshop, "playwood m-01 RIZING")
    sck = Keyword_builder().build(PLATFORM.yahooshop, "playwood sck RIZING")
    sc = Keyword_builder().build(PLATFORM.yahooshop, "playwood sc RIZING")
    
    searchs = [m_1000, m_3000, m_6011, m_6021, m_7001, m_611, m_2001, m_4000, m_5000, xg_series, 
               b_series, xb_series, m_101, m_201, m_301, m_401, m_501, m_801, m_901, two_tone, m_01, sck, sc]
    
    combine_prods = Keyword_builder().build(PLATFORM.yahooshop, "combine")
    for search in searchs:
        search.get_all_page_elements(write_to_txt=False) ### 可以控制 各個小search_obj 有沒有需要存個別的prods.txt，要注意有存的話會多很多資料夾很雜喔！
        search.sort_by_key(sort_key="prod_title")
        combine_prods.containor.prods +=  search.containor.prods
    combine_prods.use_c_write_to_word(restart_img=False)
    
    
exp5_manually_search_RIZING_mallet()
####################################################################################################################################
### 一些以前的例子，還是保留一下好了，以後忘記怎麼 簡單的寫可以參考看看～～
### 從 step0 可以找到 適合的 keyword 和 平台，這裡就可專心 寫成word囉！
# def step1a_download_prods_and_write_file(keyword_obj):
#     keyword_obj.get_all_page_elements() 
#     RW_to_file.write_MogonSearch_obj(keyword_obj) ### 把 shop.prods 存入檔案

# def step1b_read_from_file_and_download_imgs(keyword_obj):
#     RW_to_file.read_MogonSearch_obj(keyword_obj) ### 取得 之前存的 shop.prods 檔案
#     keyword_obj.get_all_page_prods_img()

# def step1c_read_from_file_and_write_to_word(keyword_obj):
#     RW_to_file.read_MogonSearch_obj(keyword_obj) ### 取得 之前存的 shop.prods 檔案
#     RW_to_file.write_MogonSearch_to_word(keyword_obj)

# def step1_combine(keyword_obj): ### 因為各階段容易出錯，所以分成abc三個function，不想做哪段註解掉即可！
#     # step1a_download_prods_and_write_file(keyword_obj)
#     # step1b_read_from_file_and_download_imgs(keyword_obj)
#     step1c_read_from_file_and_write_to_word(keyword_obj)

# playwood_rizing = Keyword_builder().build( PLATFORM.yahooshop, "playwood RIZING") ### 建立 key_at_yahooshop，但爬下來沒有且不像樂器店
# step1_combine(playwood_rizing)