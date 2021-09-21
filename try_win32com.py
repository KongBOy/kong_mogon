import os
from win32com import client
### word的操作全部都要是 絕對路徑喔！
cur_path = os.getcwd()
######################################################################################################
### 可參考：https://www.youtube.com/watch?v=k7z-pQAzTnI&list=PLPCzOUVRzMMib6plz_Su32H0VrdaQ3UnQ
word = client.gencache.EnsureDispatch('word.application')
word.Visible = 1
word.DisplayAlerts = 0
doc = word.Documents.Add()


######################################################################################################
range1 = doc.Range(0, 0)
grid_row_amount = 5  #len(search_obj.containor.prods) + 1  ### +1 for title
grid_col_amount = 4
table = doc.Tables.Add(range1, grid_row_amount, grid_col_amount)  ### 加入表格
######################################################################################################
'''
官方 VBA 的 API，但好像跟python超像： https://docs.microsoft.com/zh-tw/office/vba/api/word.cells.merge
各enum數值的樣子：https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2003/aa211923(v=office.11)
'''
### 方法1：像是用滑鼠 點第一格，往右拖三格，然後按合併
### 參考來源：選取、合併的例子： https://zhidao.baidu.com/question/919851014487357619.html
### 優點：自由度超高，缺點：寫起來較麻煩
# table.Cell(1, 1).Range.Select()
# word.Selection.MoveRight(Count=3, Extend=1)  ### 可參考：https://docs.microsoft.com/zh-tw/office/vba/api/word.selection.moveright, Extend參數可參考：https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2003/aa211923(v=office.11)#wdmovementtype
# word.Selection.Cells.Merge()                 ### 可參考：https://docs.microsoft.com/zh-tw/office/vba/api/word.cells.merge
# word.Selection.Cells.Shading.Texture = 200   ### 數值越大越深，可參考 https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2003/aa211923(v=office.11)#wdtextureindex

### 方法2： 後來自己研究API規律，前面的動作只是想選某一個row，可以精簡成下面
### 優點：超簡單，缺點： 目前找不到方法 只選取 Rows裡面的 特定 col
table.Rows(1).Cells.Merge()


### 背景灰色網底
table.Cell(1, 1).Shading.Texture = 200   ### 數值越大越深，可參考 https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2003/aa211923(v=office.11)#wdtextureindex
### 垂直置中
table.Cell(1, 1).VerticalAlignment = 1
### 框線
table.Rows(2).Borders.InsideLineStyle = 1
table.Rows(2).Borders.OutsideLineStyle = 1
### 字形
table.Cell(1, 1).Range.Font.Name = "Arial"
print(dir(table.Cell(1, 1).Range))

### 填字
### 方法1：
table.Cell(1, 1).Range.InsertAfter("Title")
table.Cell(2, 1).Range.InsertAfter("Product_name")
table.Cell(2, 2).Range.InsertAfter("Product_price")
table.Cell(2, 3).Range.InsertAfter("Product_link")
table.Cell(2, 4).Range.InsertAfter("Product_image")

### 方法2：不小心試出來的
### table.Cell(1, 1).Range.Text = "Title"


# for go_prod, prod in enumerate(search_obj.containor.prods):
#     table.Cell( 2 + go_prod, 1 ).Range.InsertAfter(prod.prod_title)
#     table.Cell( 2 + go_prod, 2 ).Range.InsertAfter(prod.price)
#     table.Cell( 2 + go_prod, 3 ).Range.InsertAfter(prod.prod_url)
#     # print(search_obj.result_imgs_dir + "/" + "%04i.jpg"%(go_prod + 1))
#     table.Cell( 2 + go_prod, 4 ).Range.InlineShapes.AddPicture(cur_path + "/" + search_obj.containor.result_imgs_dir + "/" + "%04i.jpg" % (go_prod + 1),False,True)
#     print("docx row:%04i finished~~" % go_prod)
# doc.SaveAs( cur_path + "/" + search_obj.containor.result_dir + "/containor.docx")
# doc.SaveAs( "temp.docx")
# doc.Close()
# # word.Quit()
