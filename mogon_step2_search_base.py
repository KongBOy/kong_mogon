import time

from RW_util import RW_to_file
from mogon_step1_scraper import Products, Mogon_Scraper_util
import sys
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from build_dataset_combine import Check_dir_exist_and_build
from util import get_dir_certain_file_name

from search_base import Search_base

#############################################################################################################################################
from enum import Enum, auto
class PLATFORM(Enum):
    jraku = "jrakutenshopping"
    yahoobid = "jyahoobid"
    yahooshop = "jyahooshopping"
plat_jraku = PLATFORM.jraku
plat_yahoobid = PLATFORM.yahoobid
plat_yahooshop = PLATFORM.yahooshop

#############################################################################################################################################
class MogonSearch_obj(Search_base):
    def __init__(self, base_url, result_dir):
        super().__init__(base_url, containor=Products(result_dir=result_dir), Mogon_Scraper_util)


    def __str__(self):
        prod_string = ""
        for go_prod, prod in enumerate(self.containor.prods): prod_string += f"%04i {prod.prod_title}\n" % go_prod
        return prod_string

    #############################################################################################################################################
    ### get_all_page_elements 已經抽出來寫進 Search_base 裡面囉！

    #############################################################################################################################################
    ### products 還有 產品影像部分，這個就在這裡個別implement囉！
    def get_all_page_prods_img(self, prod_num=True, prod_title=False, shop_name=False, price=False):
        if(self.containor.prods == []) : self.get_all_page_elements()  ### 如果 prods是空的，就先去抓 prods囉！
        Check_dir_exist_and_build(self.containor.result_imgs_dir)  ### 建立 imgs資料夾
        Mogon_Scraper_util.get_prods_image(self.containor, start_index=0, prod_num=prod_num, prod_title=prod_title, shop_name=shop_name, price=price)

    #############################################################################################################################################
    def sort_by_key(self, sort_key):
        if(sort_key == "shop_name" ): self.containor.prods = sorted(self.containor.prods, key=lambda prod: prod.shop_name)
        if(sort_key == "price"     ): self.containor.prods = sorted(self.containor.prods, key=lambda prod: prod.price)
        if(sort_key == "prod_title"): self.containor.prods = sorted(self.containor.prods, key=lambda prod: prod.prod_title)

    #############################################################################################################################################
    def _check_prods_in_ram_or_file(self, sort_key=None):
        import os
        if(len(self.containor.prods) == 0):  ### 如果 現在products是空的 且 之前有存檔過prods.txt 才去抓資料喔， products不是空的在抓資料 這可能是自己操作失誤，從網路抓 又從 檔案讀，總共抓了兩次 ，下載的img就重複了喔！
            print("目前 RAM 內沒有 containor 資料")
            if(os.path.isfile(self.containor.result_dir + "/prods.txt")):  ### 先看看有沒有上次的紀錄，沒有再從網路上重新抓
                print("有上次的products資料，讀取上次的資料")
                RW_to_file.read_MogonSearch_obj(self)  ### 取得 之前存的 search_obj 抓到的 prods檔案
                self.sort_by_key( sort_key )
            else:  ### 沒有上次的紀錄，從網路上重新抓，順便存起來
                print("沒有products資料檔，重新從網路抓資料")
                self.get_all_page_elements()
                self.sort_by_key( sort_key )
                RW_to_file.write_MogonSearch_obj(self)

    def _check_imgs_downloaded(self, sort_key=None):
        file_names = get_dir_certain_file_name(self.containor.result_imgs_dir, ".jpg")
        print("file_names", file_names)
        if( len(file_names) == 0 ):  ### 如果 prods_imgs資料夾下面是空的，用use_b去下載imgs
            print("圖片還沒有下載，現在自動去下載 RAM內products 的 imgs 囉！")
            self.sort_by_key( sort_key )
            self.use_b_download_prods_img()
        print("containor 和 imgs 都存在")

    #############################################################################################################################################
    def use_a_download_prods_and_write_file(self, restart_url=False, sort_key=None):
        if  (restart_url is True):
            self.get_all_page_elements()  ### 直接從 網路上抓products
            self.sort_by_key( sort_key )
            RW_to_file.write_MogonSearch_obj(self)  ### 把 search_obj 抓到的 prods 存入檔案
        elif(restart_url is False): self._check_prods_in_ram_or_file()  ### 先看看之前的prods紀錄，有的話讀取之前的prods，沒有的話重新從網路上抓prods並存入檔案


    def use_b_download_prods_img(self, restart_url=False, prod_num=True, shop_name=False, price=False, prod_title=False, sort_key=None):
        if(restart_url is True):  ### 直接重新抓prods
            self.use_a_download_prods_and_write_file(restart_url=True, sort_key=sort_key)  ### 直接從 網路上抓products 並 存入檔案
        elif(restart_url is False):  ### 先看看之前的prods紀錄，有的話讀取之前的prods來抓prods_img，沒有的話重新從網路上抓prods並存入檔案
            self.use_a_download_prods_and_write_file(restart_url=False, sort_key=sort_key)  ### 先看看以前 有沒有存過 prods.txt，有的話就用之前的prods.txt紀錄，沒有的話 重新從網路上抓 並存入檔案
        self.get_all_page_prods_img( prod_num=prod_num, prod_title=prod_title, shop_name=shop_name, price=price)  ### 抓prods_img


    def use_c_write_to_word(self, restart_url=False, restart_img=False, sort_key=None):
        Check_dir_exist_and_build(self.containor.result_dir)       ### 建立資料夾
        Check_dir_exist_and_build(self.containor.result_imgs_dir)  ### 建立資料夾
        if(restart_url is True):  ### 直接重新抓prods 和 prods_img
            self.use_b_download_prods_img(restart_url=True, sort_key=sort_key)
        elif(restart_url is False):
            ### 請注意，這裡的 _check 沒有保證 prods.txt 和 prods_img 有對應喔！如果想對應要再多寫function，或用下面的elif
            if  (restart_img is True):  ### 根據 prods 重新下載 prods_img！但是如果有3000張影像，每次要重新下載很麻煩，如果之前已下載過 且 事前已經確認 prods_img 和 prods.txt 是對應的，可以用elif直接寫docx
                self.use_b_download_prods_img(restart_url=False, sort_key=sort_key)
            elif(restart_img is False):  ### 如果存在 prods.txt 和 prods_img，就直接寫docx(但不保證 prods.txt 和 prods_img 對應關係，請事前確認)
                self._check_prods_in_ram_or_file(sort_key=sort_key)  ### 先看看之前的prods紀錄，有的話讀取之前的prods來抓prods_img，沒有的話重新從網路上抓prods並存入檔案
                self._check_imgs_downloaded(sort_key=sort_key)       ### 先看看之前的prods_img資料夾是不是空的，空的話就重新下載，非空不做事，也要注意一下不保證存在的imgs 和 目前的 prods 是有對影的喔，用前請先自行確認一定對應
        RW_to_file.write_MogonSearch_to_word(self)  ### 寫docx
