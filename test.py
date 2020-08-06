
from selenium import webdriver
import pymongo
import bs4 as bs
import requests
import threading

op = webdriver.firefox.options.Options()
op.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference("javascript.enabled", True)




def get_db():

    client = pymongo.MongoClient("localhost",27017)
    return client['trackerdb']



def job(input_data):

	print("@ job ",input_data[0],"\n",input_data[1],"\n",input_data[2])


	browser = webdriver.Firefox(profile,options=op)
	browser.get(input_data[1])
	page_contents = browser.page_source
	soup = bs.BeautifulSoup(page_contents, 'html.parser')
	print(soup.find('span', id="productTitle").text.strip())
	print(soup.find('div',id='availability').text.strip())

	price = soup.find('span',id='priceblock_ourprice')

	if price is None:
		price = soup.find('span',id='priceblock_dealprice')

	if price is None:
		price = soup.find('span',id='priceblock_saleprice')
	
	print(price.text.strip())




def main():

    try:

        mydb = get_db()

        email_col = mydb["email_collection"]

        emailids = email_col.find({})

        for i in emailids:

            print("@ ",i['_id'])

            mycol = mydb[i['_id']]

            my_urls = mycol.find({})

            if mycol.estimated_document_count() is 0:

                mycol.drop()
                email_col.delete_one({"_id":i['_id']})
                print("deleted ",i['_id'])

            else :

                for j in my_urls:


                    arg=(i['_id'],j['url'],j['price']);

                    threading.Thread(target=job, args=(arg,)).start()     
        
    except Exception as e:
        
        print("Error :: ",e)
    



while True:

    main()
    break
    print("time to sleep")
    time.sleep(1800)
    break