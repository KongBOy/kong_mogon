import time

from ithelp_step1_scraper import Day_infos, Ithelp_scraper_util
from search_base import Search_base

import sys 
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from build_dataset_combine import Check_dir_exist_and_build

from RW_util import RW_to_file

class IthelpSearch_obj(Search_base):
    def __init__(self, base_url, result_dir):
        super().__init__(base_url=base_url, containor=Day_infos(result_dir=result_dir), scraper_util=Ithelp_scraper_util)
        self.page_symbol = "?"

    def __str__(self):
        day_infos_string = ""
        for go_day_info, day_info in enumerate(self.containor.day_infos): day_infos_string += f"%04i {day_info.title}\n"%go_day_info
        return day_infos_string

    #############################################################################################################################################
    ### get_all_page_elements 已經抽出來寫進 Search_base 裡面囉！

if(__name__=="__main__"):
    tensorflow30day = IthelpSearch_obj(base_url="https://ithelp.ithome.com.tw/users/20119971/ironman/2254", result_dir = "it30day/tensorflow30day")
    tensorflow30day.get_all_page_elements(write_to_txt=False)
    Check_dir_exist_and_build("tensorflow30day")
    RW_to_file.write_IthelpSearch_obj(tensorflow30day)

    tensorflow30day_good = IthelpSearch_obj(base_url="https://ithelp.ithome.com.tw/users/20112126/ironman/2841", result_dir = "it30day/tensorflow30day_good")
    tensorflow30day_good.get_all_page_elements(write_to_txt=False)
    Check_dir_exist_and_build("tensorflow30day_good")
    RW_to_file.write_IthelpSearch_obj(tensorflow30day_good)