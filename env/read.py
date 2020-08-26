
# Reading an excel file using Python 
import xlrd 
  
# Give the location of the file 
loc = ("number.csv") 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
sheet.cell_value(0, 0)




import openpyxl
wb = openpyxl.load_workbook('number.xlsx')
wb.get_sheet_names()



 for rowOfCellObjects in sheet['A1':'C3']:
 	for cellObj in rowOfCellObjects:
 		print(cellObj.coordinate,coordinate,cellObj.value)
 		print('---end of row---')



	for rowOfCellObjects in sheet['A1':'B2']:
for cellObj in rowOfCellObjects:
	               print(cellObj.coordinate, cellObj.value)
	                          



import openpyxl, pprint
wb = openpyxl.load_workbook('/home/priya/Documents/number.xlsx')          
sheet = wb.get_sheet_by_name('Sheet1')
print(sheet.cell(8).value)
print(sheet.nrows)
print(sheet.ncols)




d = {}
wb = openpyxl.load_workbook('/home/priya/Documents/number.xlsx')          
sheet = wb.get_sheet_by_name('Sheet1')
for i in range(1,8):
	cell_value_Name = sheet.cell(1,1).value
	cell_value_age = sheet.cell(2,2).value
	d[cell_value_Name] = cell_value_age
	print(i,sheet.cell(row=1,column=1).value)
	dict_list.append(d)
	print(dict_list)
	print(d)



    
for i in range(1,8):
	print(i,sheet.cell(row=1,column=8).value)






import openpyxl, pprint
wb = openpyxl.load_workbook('/home/priya/Documents/number.xlsx')          
sheet = wb.get_sheet_by_name('Sheet1')
countyData = {}
print('Reading rows...')
for row in range(sheet.max_row ):
	Name= sheet['A' + str(row)].value
	age= sheet['B' + str(row)].value
	data_list={'intents':data_list}
	j=json.dumps(data_list)
	with open('dat')



pip install simplejson


import xlrd
from collections import OrderedDict
import simplejson as json
# Open the workbook and select the first worksheet
wb = openpyxl.load_workbook('/home/priya/Documents/number.xlsx')
sh = wb.sheet_by_index(0)
number_list = []
for rownum in range(1, sh.nrows):
    number = OrderedDict()
    row_values = sh.row_values(rownum)
    number['Name'] = row_values[0]
    number['age'] = row_values[1]
    number_list.append(cars)
j = json.dumps(number_list)
with open('data.json', 'w') as f:
    f.write(j)




import pandas
import os
os.chdir('/home/priya/Documents/number.xlsx')
print(pandas.read_csv('number.xlsx'))




using openpyxl:
d={}
for i  in range(sheet.max_row+1):
	Name = sheet.cell(row= i,column=1).value
	age=sheet.cell(row =i,column=2).value
        
        


import openpyxl, pprint
wb = openpyxl.load_workbook('/home/priya/Documents/number.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')
keys = [sheet.cell(2, col_index).value for col_index in range(0,2)]
print (keys)
dict_list = []
d = {}
for row_index in range(1, xl_sheet.nrows):
	for col_index in range(0,8):
		d = {keys[col_index]: xl_sheet.cell(row_index, col_index).value
		for col_index in range(0,8)}
		dict_list.append(d)
		print (dict_list)


d=[]
for i in range(1,8):
	d.append(str(i))
	print(',',join(d))





	print(i,sheet.cell(row=i,column=1).value)
	












wb = xlrd.open_workbook('foo.xls')
sh = wb.sheet_by_index(2)   
for i in range(138):
    cell_value_class = sh.cell(i,2).value
    cell_value_id = sh.cell(i,0).value




d = {}
import xlrd 
loc = ('/home/priya/Documents/number.xlsx') 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(1,8)
for i in range(1,8):
	print(sheet.row_values(1))
	dict_list.append(d)
	print(dict_list)
# print(sheet.column_values(1)) 


dic = pandas.read_excel(excelfile).columns



def home(request):
    user_count = User.objects.count()
    client_count = Client.objects.count()
    return Response({
        'user_count' : user_count,
        'client_count' : client_count,
    })



     python manage.py startapp candidate