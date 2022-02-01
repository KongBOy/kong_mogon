from abc import abstractmethod

import sys
sys.path.append(r"C:\Users\TKU\Desktop\kong_model2\kong_util")

#############################################################################################################################################
### 定義爬下來的東西 長什麼樣子
###     舉例這可以是 Product
class BaseData:
    @abstractmethod
    def __str__(self): pass  ### 寫進去txt的時候會用這個喔！

#############################################################################################################################################
### 定義 操作 爬下來的東西 的介面
### 舉例這可以是一個 "操作Product介面"的概念~~~不實做，是給 需要操作product 的物件 繼承用的喔！實作部分在Products內
class BaseData_Browser:
    @abstractmethod
    def add_BaseData(self): pass

    @abstractmethod
    def read_BaseData_from_file(self, path): pass

    ### write 丟給 RW_util做囉


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
    @abstractmethod
    def get_page_amount(in_url): pass

    @staticmethod
    @abstractmethod
    def get_page_element(in_url, containor, series=None): pass
