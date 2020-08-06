import pymongo #python client for mongodb

myclient = pymongo.MongoClient("mongodb://localhost:27017/") #localhost server
mydb = myclient["trackerdb"] #selecting trackerdb database 

myclient.drop_database("trackerdb") #clearing previous entries

email_coll = mydb["email_collection"]  #selecting collection "email_collection"

#list of emailid to be uploaded
email_list = ["surajsinghrana7417@gmail.com","myemailid7417@gmail.com","uploadhoja@gmail.com"]

#iterating over email_list
for i in email_list:

	#inserting email as primary id
	email_coll.insert_one({'_id':i})


col_list = email_coll.find({})

for i in col_list:

	usr_col = mydb[i['_id']]

	usr_col.insert_one({"url":"https://www.amazon.in/CHKOKKO-Active-Regular-Stretchable-Tshirts/dp/B07NSX5VGQ/ref=bbp_bb_d33a38_st_bGHZ_w_0?psc=1&smid=A2N8QJKMP57BXU","price":1200})

	usr_col.insert_one({"url":"https://www.amazon.in/dp/B07NV9YH7W/ref=twister_dp_update?_encoding=UTF8&psc=1","price":1000})
