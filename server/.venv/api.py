from flask import Flask, jsonify, request
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from pymongo import MongoClient

from datetime import datetime
from zoneinfo import ZoneInfo

from webscraper import WebScraper

import re

app = Flask(__name__)

@app.route("/search", methods = ['POST'])
def search():
    product_name = request.json.get("productName")
    
@app.route("/price_values", methods = ['POST'])
def get_price_values():
    item = request.json.get("itemName")
    object = WebScraper(item)
    object.price_values()

@app.route("/test")
def test():
    return jsonify("hi")

@app.route("/product_information", methods = ['POST'])
def get_product_information():
    item = request.json.get("itemName")

    if not item:
        return(jsonify({"Message": "You must include an item"}),400)
        

    object = WebScraper(item)
    return jsonify(object.product_information)
        


if __name__ == "__main__":
    app.run(debug=True, port=8080)

