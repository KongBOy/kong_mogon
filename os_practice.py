import os

### os.path()
print("os.path()")
print(os.path)
print(type(os.path))
print()

### os.getcwd()
print("os.getcwd()")
print(os.getcwd())
print(type (os.getcwd()))
print("the true string:",repr(os.getcwd()))
print()

### os.listdir()
print("os.listdir()")
print(os.listdir("C:\\Users\\may\\Desktop\\mogon\\mogon_mallet"))
print(type(os.listdir("C:\\Users\\may\\Desktop\\mogon\\mogon_mallet")))
print()

### conbine os.getcwd() and os.listdir()
print(os.listdir(os.getcwd()))
print()

### os.path.isdir()
print("os.path.isdir()")
for item in os.listdir("C:\\Users\\may\\Desktop\\mogon\\mogon_mallet"):
    print("Is" , item , "a directory? :",os.path.isdir(item))
print()

### os.path.isfile()
print("os.path.isfile()")
for item in os.listdir("C:\\Users\\may\\Desktop\\mogon\\mogon_mallet"):
    print("Is" , item , "a file? :",os.path.isfile(item))
print()

### os.path.split()
print("os.path.split()")
for item in os.listdir("C:\\Users\\may\\Desktop\\mogon\\mogon_mallet"):
    print(os.path.split(item))
print()

### os.path.splitext()
print("os.path.splitext()")
for item in os.listdir("C:\\Users\\may\\Desktop\\mogon\\mogon_mallet"):
    print(os.path.splitext(item))
print()

### os.path.exists()
for item in os.listdir(os.getcwd()):
    print("Is",item , " exist in",os.getcwd(),":",os.path.exists(item))

### os.makedirs()


all_shop_dir_name = "shop"
if( not(os.path.exists(all_shop_dir_name) ) ):
    print("directory "+ all_shop_dir_name + " does not exist")
    os.makedirs(all_shop_dir_name)
    print("make " + all_shop_dir_name + " the direcroty~~~")
else:
    print("the directory exists")

cur_path = os.getcwd()
all_shop_dir = cur_path + "\\" + all_shop_dir_name
in_dir_file_name = os.listdir(all_shop_dir)

shop_dir_name = "shop1"
if( not(shop_dir_name in in_dir_file_name) ):
    os.makedirs(all_shop_dir + "\\" + shop_dir_name )

### prep(os.getcwd())




'''
sucess!!!
'''
dir_name = "shop"
sub_dir_name = dir_name
in_data    = [{dir_name:[{sub_dir_name:"main_log"},
                         {sub_dir_name:"items_list"},
                         {sub_dir_name:"image"},
                         {sub_dir_name:"word"}]}]
print( list(in_data[0].keys())[0] )
print( (in_data[0].items()))


dir_name1 = "shop1"
sub_dir_name1 = dir_name1

dir_name2 = "shop2"
sub_dir_name2 = dir_name2
in_data2   =[ {dir_name1:[{sub_dir_name1:"main_log"},
                      {sub_dir_name1:"items_list"},
                      {sub_dir_name1:"image"},
                      {sub_dir_name1:"word"}]},
              {dir_name2:[{sub_dir_name2:"main_log"},
                      {sub_dir_name2:"items_list"},
                      {sub_dir_name2:"image"},
                      {sub_dir_name2:"word"}]}]




cur_path = os.getcwd()
dir_str = []
next_level = []
have_next_level = True
if( type(in_data2) == type(list()) ):
    cur_dir = []
    cur_dir = [] + in_data2
    next_dir = []
    while( have_next_level == True):
        for dir_item in cur_dir:
            cur_dir_name = list(dir_item.keys())[0]
            next_dir_info = dir_item[cur_dir_name]
            print("next_dir_info:",next_dir_info)
            print(type(next_dir_info))
            if(   type(next_dir_info) == type(None)  ):
                print("next_dir_info is None")
            elif( type(next_dir_info) == type("str")  ):
                print("next_dir_info is string")
                cur_dir_name += "\\" + next_dir_info
            elif( type(next_dir_info) == type(list())  ):
                print("next_dir_info is list")
                next_dir_link = []
                for next_item in next_dir_info:
                    dir_link_dict = {}
                    dir_link_key = cur_dir_name
                    dir_link_value = next_item[cur_dir_name]
                    dir_link_dict[dir_link_key] = dir_link_value
                    next_dir_link.append( dir_link_dict )
                next_dir.append(next_dir_link)
                print("next_dir:",next_dir)
            dir_str.append(cur_dir_name)
        if(len(next_dir) == 0):
            have_next_level = False
        elif(len(next_dir) > 0):
            have_next_level = True
            cur_dir = next_dir[0]
            del next_dir[0]
    print("final:",dir_str)


###for tocken in dir_str:
###    os.makedirs(cur_path + "\\" + tocken)

'''
in_data2   =[ {shop1:[{shop1_name:"main_log"},
                      {shop1_name:"items_list"},
                      {shop1_name:"image"},
                      {shop1_name:"word"}]},
              {shop2:[{shop2_name:"main_log"},
                      {shop2_name:"items_list"},
                      {shop2_name:"image"},
                      {shop2_name:"word"}]}]

'''

a = ["abc",2,"cdde"]
b = ["abc",3,"cdde"]
print(a == b)

c = "a    b "
c.replace(" ","")
print(c)
