import ver
import bs4 as bs
import time
import yagmail
import keyring
import smtplib
import threading
from selenium import webdriver
import pymongo
import requests

op = webdriver.firefox.options.Options()
op.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference("javascript.enabled", True)
browser = webdriver.Firefox(profile,options=op)


def get_db():

    client = pymongo.MongoClient("localhost",27017)
    return client['trackerdb']


def feed_db(input_data):

	my_db = get_db()
	email_coll = my_db["email_collection"]

	email_list = email_coll.find({"_id":input_data[0]})

	exists = False
	for i in email_list:

		print(input_data[0]," already exists")
		exists=True
		break
	if exists is False:
		print(input_data[0]," inserted")
		email_coll.insert_one({"_id":input_data[0]})
		
	my_coll = my_db[input_data[0]]
	my_coll.insert_one({"url":input_data[1],"price":input_data[2]})


def check_url(url):
	if url.find("https://www.amazon.in") is not 0 or url.find('B0') is -1:
		return False
	try:
		requests.get(url)

	except Exception:
		return False

	return True

def send_mail(product_title, avail, price, url, reciever_email_id):
    print("@@@ " + reciever_email_id)
    print(avail)
    print(price)
    print(url)
    print(" *** working on email ***")

    GMAIL_USERNAME = "amtrackerbhai@gmail.com"
    GMAIL_PASSWORD = "*******"

    recipient = reciever_email_id
    body_of_email = "Hurry!!! your product " + product_title + " is " + avail + " at Rs " + str(price) + "\n" + "Product Link " + url
    email_subject = " product availability" + product_title

    headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                           "subject: " + email_subject,
                           "to: " + recipient,
                           "content-type: text/html"])

    mail_content = headers + "\r\n\r\n" + body_of_email

    yagmail.register(GMAIL_USERNAME, GMAIL_PASSWORD)

    yag = yagmail.SMTP(GMAIL_USERNAME)

    yag.send(to=recipient, subject=email_subject, contents=mail_content)

    print("*** done with email ***")

    return True



def job(input_data):

    print("@ job ",input_data[0],"\n",input_data[1],"\n",input_data[2])
    url = input_data[1]
    your_price = int(input_data[2])
    reciever_email_id = input_data[0]

    browser.get(input_data[1])
    page_contents = browser.page_source
    soup = bs.BeautifulSoup(page_contents, 'html.parser')

    product_title=soup.find('span', id="productTitle").text.strip()

    avail = soup.find('div',id='availability').text.strip()
    if(avail.find('In stock.')):
        avail='In stock.'
    elif(avail.find('Only 1 left in stock.')):
        avail = 'Only 1 left in stock.'
    elif (avail.find('Only 2 left in stock.')):
        avail = 'Only 2 left in stock.'
    elif (avail.find('Only 3 left in stock.')):
        avail = 'Only 3 left in stock.'
    elif (avail.find('Currently unavailable.')):
        avail = 'Currently unavailable.'
    else:
        print("NOT IN STOCK")

    price = soup.find('span',id='priceblock_ourprice')
    if price is None:
        price = soup.find('span',id='priceblock_dealprice')
    if price is None:
        price = soup.find('span',id='priceblock_saleprice')
    
    price = price.text.strip()
    price = price.replace(",", "")
    price = int(float(price[2:]))

    if price <= your_price:

        print("Price decreased book now")
        return send_mail(product_title, avail, price, url, reciever_email_id)

    else:
        print("Price is high please wait for the best deal")

        feed_db(input_data)

        return False
         

def main(args):

	sab_h=args.split()
	input_data=set()
	reciever_email_id=inputAddress =sab_h[0]
	#print(inputAddress)
	if(ver.verify_email(inputAddress)):
		k=0;
		for i in sab_h[1:]:
			if(k%2==1):
				your_price=i
				node= (reciever_email_id,url, your_price)
				#print (your_price)
				input_data.add(node)
			else:
				url=i
				#print (url)
				if check_url(url) is False:
					print("given", url," is INVALID")
					
			k+=1
	else:
		print("given email addresss is incorrect")
		return False

	#main_script.main()
	print("now working on ur requests")

	for j in input_data :
	    
	    threading.Thread(target=job, args=(j,)).start()
	    

	print("main end") 


