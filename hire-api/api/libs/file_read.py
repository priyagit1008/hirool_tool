
filenames = ['menu_sidebar.json', 'user_columns.json', 'user_designation.json']
data = {}

    for name in filenames:
        with open(name) as f:
            key = name.partition('.')[0]
            data[key] = f.read()

 # file_path = os.path.join(str(filenames))
 # for name in filenames:
 # 	myfile= open(file_path,'r')
 # 	jsondata = myfile.read()
 # 	obj = json.loads(jsondata)
 # 	return Response(obj)