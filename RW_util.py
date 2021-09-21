class RW_to_file:
    @staticmethod
    def write_soup_to_file(soup, file_name):  ### 把整個 soup寫進html來看 比較好看
        import codecs
        f = codecs.open(file_name + ".html", "w", "utf-8")
        f.write(str(soup))
        f.close()

    @staticmethod
    def write_IthelpSearch_containor(search_obj):
        with open( search_obj.result_dir + "/it30days_full_info.txt" , "w" , encoding = "utf8") as f:
            for go_day_info, day_info in enumerate(search_obj.containor.day_infos):
                f.write(str(day_info))
                if(go_day_info != len(search_obj.containor.day_infos) - 1): f.write("\n")  ### 除了最後一個product外都要換行

    @staticmethod
    def write_IthelpSearch_obj(search_obj):
        with open( search_obj.result_dir + "/it30days_just_title.txt" , "w" , encoding = "utf8") as f:
            f.write(str(search_obj))
            


    @staticmethod
    def write_MogonSearch_obj(search_obj):
        with open( search_obj.result_dir + "/prods.txt" , "w" , encoding = "utf8") as f:
            for go_prod, prod in enumerate(search_obj.containor.prods):
                f.write(str(prod))
                if(go_prod != len(search_obj.containor.prods) - 1): f.write("\n")  ### 除了最後一個product外都要換行


    @staticmethod
    def read_MogonSearch_obj(search_obj):
        search_obj.containor.read_prods_from_file( path=search_obj.result_dir + "/prods.txt" )


    @staticmethod
    def write_MogonSearch_to_word(search_obj):
        import os
        from win32com import client
        ### word的操作全部都要是 絕對路徑喔！
        cur_path = os.getcwd()

        word = client.gencache.EnsureDispatch('word.application')
        word.Visible = 1
        word.DisplayAlerts = 0
        doc = word.Documents.Add()

        range1 = doc.Range(0, 0)

        grid_row_amount = len(search_obj.containor.prods) + 1  ### +1 for title
        grid_col_amount = 4

        table = doc.Tables.Add(range1, grid_row_amount, grid_col_amount)
        table.Cell(1, 1).Range.InsertAfter("Product_name")
        table.Cell(1, 2).Range.InsertAfter("Product_price")
        table.Cell(1, 3).Range.InsertAfter("Product_link")
        table.Cell(1, 4).Range.InsertAfter("Product_image")

        for go_prod, prod in enumerate(search_obj.containor.prods):
            table.Cell( 2 + go_prod, 1 ).Range.InsertAfter(prod.prod_title)
            table.Cell( 2 + go_prod, 2 ).Range.InsertAfter(prod.price)
            table.Cell( 2 + go_prod, 3 ).Range.InsertAfter(prod.prod_url)
            # print(search_obj.result_imgs_dir + "/" + "%04i.jpg"%(go_prod + 1))
            table.Cell( 2 + go_prod, 4 ).Range.InlineShapes.AddPicture(cur_path + "/" + search_obj.containor.result_imgs_dir + "/" + "%04i.jpg" % (go_prod + 1), False, True)
            print("docx row:%04i finished~~" % go_prod)
        doc.SaveAs( cur_path + "/" + search_obj.containor.result_dir + "/containor.docx")
        doc.Close()
        # word.Quit()
