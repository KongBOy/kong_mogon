from RW_util import RW_to_file
from mogon_step2_search_base import PLATFORM , MogonSearch_obj
import datetime

class Keyword(MogonSearch_obj):
    def __init__(self):
        self.platform = None     ### 基本
        self.keyword = None      ### 基本
        self.keyword_url = None  ### 由上兩個基本來設定
        self.series = None  ### 2021/09/12 新加的attr

        self.result_dir = None    ### 設定 Keyword的prods_dir放哪裡

    def _init_super_search_obj(self, base_url, result_dir):  ### 初始化 search_obj ( 建立products物件 )
        super().__init__(base_url=base_url, result_dir=result_dir, series=self.series)


class Keyword_builder:
    def __init__(self, keyword=None):
        if(keyword is None): self.keyword_obj = Keyword()
        else: self.keyword_obj = keyword

    def _build(self):
        ### 設定url
        url = f"https://www.moganshopping.com/zh_tw/public/search/searchitem.php?action={self.keyword_obj.platform.value}&keyword={self.keyword_obj.keyword}&SearchMethod=multi"
        self.keyword_obj.keyword_url = url

        ### 設定目的地資料夾
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.keyword_obj.result_dir = f"keyword_search/{self.keyword_obj.keyword}/{self.keyword_obj.platform.value}/{current_time}"

        ### 建立products物件
        self.keyword_obj._init_super_search_obj(base_url=self.keyword_obj.keyword_url, result_dir=self.keyword_obj.result_dir)

    def set_attr(self, platform, keyword, series=None):
        self.keyword_obj.platform = platform
        self.keyword_obj.keyword = keyword
        self.keyword_obj.series = series
        self._build()
        return self.keyword_obj

### dummy的寫法還是留著好了，給以後的自己當例子參考要怎麼拆開簡單寫
### example1：走訪3個平台，看看keyword能找到什麼，無腦用法 只能重新開始 爬url存成prods.txt 再 存圖，
###             如果想讀之前存的結果時， 爬url和存的兩行註解掉才可以， 要不然 總共會有 read的 和 爬下來的 prods 重複的兩份prods喔！
def exp1_visit_3_platform_download_imgs_dummy(keyword):
    key_at_jraku = Keyword_builder().set_attr( PLATFORM.jraku, keyword)  ### 建立 keyword物件
    key_at_jraku.get_all_page_elements()                    ### 爬url存成prods.txt
    RW_to_file.write_MogonSearch_obj(key_at_jraku)  ### 把 prods 存入檔案
    # RW_to_file.read_MogonSearch_obj(key_at_jraku)    ### 取得 之前存的 prods 檔案 ### 這行註解打開的話，要把前兩行註解掉喔！
    key_at_jraku.get_all_page_prods_img(prod_num=False, prod_title=True, shop_name=True, price=True)

    key_at_yahoobid = Keyword_builder().set_attr( PLATFORM.yahoobid, keyword)  ### 建立 keyword物件
    key_at_yahoobid.get_all_page_elements()                    ### 爬url存成prods.txt
    RW_to_file.write_MogonSearch_obj(key_at_yahoobid)  ### 把 prods 存入檔案
    # RW_to_file.read_MogonSearch_obj(key_at_yahoobid)    ### 取得 之前存的 prods 檔案 ### 這行註解打開的話，要把前兩行註解掉喔！
    key_at_yahoobid.get_all_page_prods_img(prod_num=False, prod_title=True, shop_name=True, price=True)

    key_at_yahooshop = Keyword_builder().set_attr( PLATFORM.yahooshop, keyword)  ### 建立 keyword物件
    key_at_yahooshop.get_all_page_elements()                    ### 爬url存成prods.txt
    RW_to_file.write_MogonSearch_obj(key_at_yahooshop)  ### 把 prods 存入檔案
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
    key_at_jraku = Keyword_builder().set_attr( PLATFORM.jraku, keyword)  ### 建立 keyword物件
    key_at_jraku.use_b_download_prods_img(restart_url=restart_url, prod_num=False, prod_title=True, shop_name=True, price=True)

    key_at_yahoobid = Keyword_builder().set_attr( PLATFORM.yahoobid, keyword)  ### 建立 keyword物件
    key_at_yahoobid.use_b_download_prods_img(restart_url=restart_url, prod_num=False, prod_title=True, shop_name=True, price=True)

    key_at_yahooshop = Keyword_builder().set_attr( PLATFORM.yahooshop, keyword)  ### 建立 keyword物件
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
    key_at_yahooshop = Keyword_builder().set_attr( platform, keyword)  ### 建立 keyword物件
    key_at_yahooshop.get_all_page_elements()                    ### 爬url存成prods.txt
    RW_to_file.write_MogonSearch_obj(key_at_yahooshop)  ### 把 prods 存入檔案
    # RW_to_file.read_MogonSearch_obj(key_at_yahooshop)    ### 取得 之前存的 prods 檔案 ### 這行註解打開的話，要把前兩行註解掉喔！
    key_at_yahooshop.get_all_page_prods_img(prod_num=False, prod_title=True, shop_name=True, price=True)
    RW_to_file.write_MogonSearch_to_word(key_at_yahooshop)
### exp用法： 給 platform 和 keyword即可
# exp3_write_to_docx_dummy( PLATFORM.yahooshop, "playwood RIZING")


####################################################################################################################################
def exp4_write_to_docx_and_use_before_things(platform, keyword, restart_url=False, restart_img=False, sort_key=None):
    key_at_yahooshop = Keyword_builder().set_attr( platform, keyword)  ### 建立 keyword物件
    key_at_yahooshop.use_c_write_to_word(restart_url=restart_url, restart_img=restart_img, sort_key=sort_key)
### exp用法： 給 platform 和 keyword即可
#  (restart_url=False, restart_img=False) ### 一開始 prods.txt和prods_img 什麼都沒有的時候 會自動重爬  或者 如果 prods.txt 和 prods_img 都已經確定好對應了，直接寫docx
#  (restart_url=True)                     ### prods.txt 和 prods_img 都重新下載，再寫 docx
#  (restart_url=False, restart_img=True)  ### 用現存的prods.txt，重新下載 prods_img，再寫 docx
### 2020/06/20 最後用這個囉！
# exp4_write_to_docx_and_use_before_things( PLATFORM.yahooshop, "playwood RIZING", restart_url=True, sort_key="prod_title")


####################################################################################################################################
def Run_searchs(searchs, save_name):
    combine_prods = Keyword_builder().set_attr(PLATFORM.yahooshop, save_name)
    for search in searchs:
        search.get_all_page_elements(write_to_txt=False)  ### 可以控制 各個小search_obj 有沒有需要存個別的prods.txt，要注意有存的話會多很多資料夾很雜喔！
        search.sort_by_key(sort_key="prod_title")
        combine_prods.containor.prods +=  search.containor.prods
    combine_prods.use_c_write_to_word(restart_img=False)

def exp5_manually_search_RIZING_mallet():
    m_1000    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-1001 RIZING"  , series="M-1000 Series (R：藤棒)")
    m_1040    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-1041 RIZING"  , series="M-1000 Series (R：藤棒)")
    m_3000    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-3000 RIZING"  , series="M-3000 Series")
    m_6011    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-6011 RIZING"  , series="M-6000 Series")
    m_6021    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-6021 RIZING"  , series="M-6000 Series")
    m_7001    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-7001 RIZING"  , series="M-7000 Series")
    m_611     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood m-611 RIZING"   , series="M-610 Series")
    m_2001    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-2001 RIZING"  , series="M-2000 Series (R：藤棒)")
    m_4000    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-4000 RIZING"  , series="M-4000 Series")
    m_5000    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-5000 RIZING"  , series="M-5000 Series")
    xg_series = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood XG RIZING"      , series="XG Series")
    b_series  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood B-1 RIZING"     , series="B Series")
    xb_series = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood XB RIZING"      , series="XB Series")
    m_101     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-101 RIZING"   , series="M-100 Series")
    m_201     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-201 RIZING"   , series="M-200 Series")
    m_301     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-301 RIZING"   , series="M-300 Series")
    m_401     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-401 RIZING"   , series="M-400 Series")
    m_501     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-501 RIZING"   , series="M-500 Series")
    m_801     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-801 RIZING"   , series="M-800 Series")
    m_901     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood M-901 RIZING"   , series="M-900 Series")
    two_tone  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood two-tone RIZING", series="Two-Tone Series")
    m_01      = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood m-01 RIZING"    , series="M-00 Series")
    sck_x_g   = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood sck-1 RIZING"   , series="SCK Series：Xylophone and Glockenspiel")
    sck_x_m   = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood sck-02 RIZING"  , series="SCK Series：Xylophone and Marimba")
    sck_m_v   = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood sck-11 RIZING"  , series="SCK Series：Marimba and Vibraphone")
    sc        = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood sc RIZING"      , series="Suspended Cymbal Mallet Series")
    bag1      = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood DTR-SET RIZING" , series="Drum Training Set")
    bag2      = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood MS-EDU-Z RIZING", series="Drum Training Set")


    searchs = [
               m_1000, m_1040, m_3000, m_6011, m_6021, m_7001, m_611, m_2001, m_4000, m_5000, xg_series,
               b_series, xb_series, m_101, m_201, m_301, m_401, m_501, m_801, m_901,
               two_tone, m_01, sck_x_g, sck_x_m, sck_m_v, sc,
               bag1, bag2
              ]
    Run_searchs(searchs, save_name="combine_mallet_20210910")
# exp5_manually_search_RIZING_mallet()



def exp5_manually_search_RIZING_timpani():
    pro_3100 = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood pro 3100 RIZING", series="Pro-3100 Classical Series (Type R：Smooth roll stick, elegant but with healthy body)")
    pro_3200 = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood pro 3200 RIZING", series="Pro-3200 Premium Series")
    pro_3300 = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood pro-3300 RIZING", series="Pro-3300 Flannel Series (Type R：Traditional German style, with heavier head)")
    pro_1000 = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood pro 1000 RIZING", series="Pro-1000 Series")
    pro_5000 = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood pro 5000 RIZING", series="Pro-5000 Series")
    pro_100  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood pro 100 RIZING", series="Pro-100 Series")
    pro_300  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood pro 300 RIZING", series="Pro-300 Series")
    pro_400  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood pro 400 RIZING", series="Pro-400 Series")
    pro_w    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood pro-w RIZING", series="Pro-W, HF, K1, K2 Series")
    pro_t    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood t-1bq RIZING", series="T-BQ Series")

    t11      = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood t11 RIZING", series="T11, 13 Series")  ### 也會搜到 t13
    t15      = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood t15 RIZING", series="T15 Series")
    tcf      = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tcf RIZING", series="TCF Series (K：Cork Core, W：Wood Core)")
    t12      = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood t12 RIZING", series="T12 Series")  ### 也會搜到 t11, t13, t15，但不完整


    tf_11    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-11 RIZING", series="TF-10, 20 Series")
    tf_12    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-12 RIZING", series="TF-10, 20 Series")
    tf_13    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-13 RIZING", series="TF-10, 20 Series")
    tf_14    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-14 RIZING", series="TF-10, 20 Series")
    tf_21    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-21 RIZING", series="TF-10, 20 Series")
    tf_22    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-22 RIZING", series="TF-10, 20 Series")
    tf_23    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-23 RIZING", series="TF-10, 20 Series")
    tf_24    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-24 RIZING", series="TF-10, 20 Series")
    tf_1pro  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-1pro RIZING", series="TF-10, 20 Series")
    tf_2pro  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-2pro RIZING", series="TF-10, 20 Series")
    tf_3pro  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-3pro RIZING", series="TF-10, 20 Series")
    tf_4pro  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-4pro RIZING", series="TF-10, 20 Series")
    tf_5pro  = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-5pro RIZING", series="TF-10, 20 Series")

    tf_1     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-1 RIZING", series="TF-0, CF Series")
    tf_2     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-2 RIZING", series="TF-0, CF Series")
    tf_3     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-3 RIZING", series="TF-0, CF Series")
    tf_4     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-4 RIZING", series="TF-0, CF Series")
    tf_5     = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-5 RIZING", series="TF-0, CF Series")
    tf_cf    = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood tf-cf RIZING", series="TF-0, CF Series")
    knx      = Keyword_builder().set_attr(PLATFORM.yahooshop, "playwood knx RIZING", series="KONEXIO KNX Series")

    searchs = [
                pro_3100, pro_3200, pro_3300, pro_1000, pro_5000, pro_100, pro_300, pro_400, pro_w, pro_t,
                t11, t15, tcf, t12,
                tf_11, tf_12, tf_13, tf_14, tf_21, tf_22, tf_23, tf_24,
                tf_1pro, tf_2pro, tf_3pro, tf_4pro, tf_5pro,
                tf_1, tf_2, tf_3, tf_4, tf_5, tf_cf,
                knx
              ]
    Run_searchs(searchs, save_name="combine_timpani")
exp5_manually_search_RIZING_timpani()


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

# playwood_rizing = Keyword_builder().set_attr( PLATFORM.yahooshop, "playwood RIZING") ### 建立 key_at_yahooshop，但爬下來沒有且不像樂器店
# step1_combine(playwood_rizing)
