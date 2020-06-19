class Keyword_util:
    def __init__(self):
        self.keyword_url = None


    ### 分成 get_all_page_prods 和 
    ###      get_all_page_prods_imgs 兩階段是因為：如果再抓多頁面時，經常被擋，如果寫在一起，就要一起全部重新開始，所以才分成兩階段喔！
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