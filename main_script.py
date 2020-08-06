import pymongo
from selenium import webdriver
import bs4 as bs
import time
import yagmail
import keyring
import smtplib
import threading

op = webdriver.firefox.options.Options()
op.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference("javascript.enabled", True)
browser = webdriver.Firefox(profile,options=op)

my_db = pymongo.MongoClient("localhost",27017)['trackerdb']
email_coll = my_db["email_collection"]


def remove_func(input_data):

    print("@ remove_func()")
    print(input_data)

    my_col = my_db[input_data[0]]
    my_col.delete_one({"url":input_data[1], "price":input_data[2]})
                



def send_mail(product_title, avail, price, url, reciever_email_id):
    print(" *** working on email ***")

    GMAIL_USERNAME = "amtrackerbhai@gmail.com"
    GMAIL_PASSWORD = "not_a_bot@123"

    recipient = reciever_email_id
    body_of_email = "Hurry!!! your product " + product_title + "\n  is  \n" + avail + "\n  Price\n  Rs " + str(price) + "\n" + "\nProduct Link \n" + url
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


def job(input_data):

    print("@ job")

    reciever_email_id = input_data[0]
    url = input_data[1]
    your_price = int(input_data[2])

    browser.get(url)
    page_contents = browser.page_source
    soup = bs.BeautifulSoup(page_contents, 'html.parser')
    
    product_title = soup.find('span', id="productTitle").text.strip()
    avail = soup.find('div',id='availability').text.strip()

    price = soup.find('span',id='priceblock_ourprice')

    if price is None:
        price = soup.find('span',id='priceblock_dealprice')

    if price is None:
        price = soup.find('span',id='priceblock_saleprice')
    
    price = price.text.strip()

    
    avail_arr = [
        'Only 1 left in stock.',
        'Only 2 left in stock.',
        'In stock.',
        'Only 3 left in stock.'
        ]

    if avail not in avail_arr:
        print("NOT IN STOCK")
        return 

    price = price.replace(",","")
    price = int(float(price[2:]))


    if price <= your_price:

        print("Price decreased book now")
        
        send_mail(product_title, avail, price,url, reciever_email_id)

        remove_func(input_data)

    else:

        print("Price is high please wait for the best deal")





def main():

    try:

        emailids = email_coll.find({})

        for i in emailids:

            print("@ ",i['_id'])

            mycol = my_db[i['_id']]

            my_urls = mycol.find({})

            if mycol.estimated_document_count() is 0:

                mycol.drop()
                email_coll.delete_one({"_id":i['_id']})
                print("deleted ",i['_id'])

            else :

                for j in my_urls:

                    arg=(i['_id'],j['url'],j['price']);

                    threading.Thread(target=job, args=(arg,)).start()     
                    # job(arg)

        
    except Exception as e:
        
        print("Error :: ",e)
    



while True:

    main()
    print("i feel sleepy")
    time.sleep(20)