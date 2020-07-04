
import time 

import sys 
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")
from build_dataset_combine import Check_dir_exist_and_build

class Search_base():
    def __init__(self, base_url, containor, scraper_util, page_symbol="&"):
        self.base_url = base_url   ### 紀錄 從哪個base_url 來抓 products
        self.containor = containor
        self.scraper_util = scraper_util
        self.result_dir = containor.result_dir
        self.page_symbol = "&"

    def get_all_page_elements(self, write_to_txt=True):
        page_amount = self.scraper_util.get_page_amount(self.base_url) ### 取得 頁數
        print("page_amount:",page_amount)
        # page_amount = 2 ### debug用
        for go_page in range(page_amount): ### 走訪每一頁，把products撈出來
            full_url = self.base_url + self.page_symbol + "page="+ str(go_page+1) ### page是從1開始
            self.scraper_util.get_page_element( full_url, self.containor ) ### 把 容器 丟進去function內 渲染，比 mogon 多了一個go_page參數喔

            print( f"{full_url} read ok!!!!")
            if(write_to_txt):
                Check_dir_exist_and_build(self.containor.result_dir)
                with open(f"{self.containor.result_dir }/main_log.txt","a") as main_log: main_log.write(full_url + " read ok!!!! \n")
            if( (go_page+1)%10 ==0): time.sleep(8) ### 怕抓太快被擋，抓10頁休息5秒