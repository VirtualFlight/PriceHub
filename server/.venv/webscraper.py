from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from pymongo import MongoClient

from datetime import datetime
from zoneinfo import ZoneInfo

import re






class WebScraper:

    def __init__ (self, item:str):
        
        ##-------------------------------------------------- Be careful when pushing to github with this -----------------------------------------------
        self.client = MongoClient('mongodb+srv://<passwordxd>@pricehubcluster.slfbx.mongodb.net/?appname=mongodb-vscode+1.8.1')
        self.db = self.client.Products
        self.collection = self.db.product_information
        self.item = item


    def test(self):
        self.collection.find().sort({'date':-1}) #sorts the date from descending order


    def scraper(self):
        '''
        Scrapes the web for 

        '''

        options = webdriver.ChromeOptions()

        options.add_experimental_option("detach",True)

        

        self.driver = webdriver.Chrome(options=options)
       

        self.actions = ActionChains(self.driver)

        self.driver.get("http://www.google.com")
        #Finding the google search bar and searching for specific item
        google_search_bar = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, "q")))
        google_search_bar.send_keys(self.item)
        google_search_bar.send_keys(Keys.ENTER)

        
        for i in range(1,4):
            name = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, f"//div[@data-pla-slot-pos='{i}']//span[@class='pymv4e']"))).text 
            price = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, f"//div[@data-pla-slot-pos='{i}']//span[@class='e10twf ONTJqd' or @class='e10twf']"))).text 
            product_link_elements = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, f"//div[@data-pla-slot-pos='{i}']//a[@class='plantl pla-unit-title-link']")))
            product_link = product_link_elements.get_attribute('href') 

            print(f"Name: {name} \n Price: {price} \n Product_link: {product_link}")

            self.database(name, price, product_link)


    def database(self, name, price, product_link):


        product = {
            "name": name,
            "price": price,
            "product_link": product_link,
            "date": datetime.now(ZoneInfo("America/New_York")),
        }

        self.collection.insert_one(product) 
    
    def price_values(self):
        # self.collection.find().sort({'name':1})
        products_list = self.db_search()
        
        product_name= []
        product_price=[]
        highest_price = 0
        lowest_price = 0
        percentage_change = 0
        current_price = 0
        counter =0 

        for item in products_list:
            if counter == 0:
                current_price = float(item['price'][1:])
                counter+=1
            product_name.append(item['name'])
            product_price.append(float(item['price'][1:]))
            lowest_price = float(item['price'][1:])

        for price in product_price:
            if price > highest_price:
                highest_price = price
            if price < lowest_price:
                lowest_price = price
            percentage_change = ((highest_price-price)/price)*100
        
        return current_price,percentage_change, lowest_price, highest_price
    

    def db_search(self):
        products_list = self.collection.find({'name': re.compile(self.item, re.IGNORECASE)}).sort({'name':1,'date':-1})
        return products_list
        
    def db_search_name_only(self):
        products_list = self.collection.find({'name': re.compile(self.item, re.IGNORECASE)}).sort({'name':1,'date':-1})
        products_name = []

        for items in products_list:
            products_name.append(items['name'])
        
        if products_name == None:
            print("No name")
            return 

        return products_name

    def product_information(self):
        products_list = self.collection.find({'name': re.compile(self.item, re.IGNORECASE)}).sort({'name':1,'date':-1})
        products_name = []
        products_price = []
        products_url = []
        products_date = []
        
        for items in products_list:
            products_name.append(items['name'])
            products_price.append(items['price'])
            products_url.append(items['product_link'])
            products_date.append(items['date'])

        #Returns only 1 item information for now
        return products_name[0], products_price[0], products_url[0], products_date[0]

        

        


        
        
object = WebScraper("dishsoap")

print(object.db_search_name_only)



