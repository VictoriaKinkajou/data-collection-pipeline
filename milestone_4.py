# this code performs web scrape on single product, saves data as dictionary in json file. Also downloads and saves product image.

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import os
import requests
import json

class Scraper():
    def __init__(self):
        self.driver = webdriver.Firefox()
        path = '/Users/victo/Drivers/geckodriver.exe'
        self.url = "https://www.ocado.com/products/la-baume-grande-olivette-selection-syrah-383208011"
        self.dict_products = {'Image': [], 'Product Name': [], 'Price': [], 'Description': [], 'Rating': [], 'Timestamp': [], 'ID': []}

    def accept_cookies(self):
        try:
            accept_cookies_button = self.driver.find_element(by=By.ID, value='onetrust-accept-btn-handler')
            accept_cookies_button.click()

        except AttributeError: 
            accept_cookies_button = self.driver.find_element(by=By.ID, value='onetrust-accept-btn-handler')
            accept_cookies_button.click()

        except:
            pass 
    
    def open_shelf(self):
        self.driver.maximize_window()
        self.driver.get(self.url)
        time.sleep(2)
        self.accept_cookies()
        time.sleep(1) 
    
    def get_image(self): #gets the image URL and adds it to dictionary
        self.open_shelf()
        image_container = self.driver.find_element(by=By.XPATH, value='//img[@class="bop-gallery__image"]')
        self.image_src = image_container.get_attribute("src")
        self.dict_products['Image'].append(self.image_src)

    def get_text(self):
        self.product_name = self.driver.find_element(by=By.TAG_NAME, value="h1").text
        self.dict_products['Product Name'].append(self.product_name)
        
        self.price = self.driver.find_element(by=By.XPATH, value='//span[@class="bop-price__per"]').text
        self.dict_products['Price'].append(self.price)
        
        self.description = self.driver.find_element(by=By.XPATH, value='//div[@class="bop-info__content"]').text
        self.dict_products['Description'].append(self.description)
        
        try:
            self.rating = self.driver.find_element(by=By.XPATH, value='//span[@itemprop="ratingValue"]').text
            self.dict_products['Rating'].append(self.rating)
            
        except:
            self.no_rating = 'NA'
            self.dict_products['Rating'].append(self.no_rating)

    def get_timestamp(self):
        self.timestamp = datetime.datetime.now()
        self.dict_products['Timestamp'].append(self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    def get_id(self):
        self.product_id = self.url[-9:]
        self.dict_products['ID'].append(self.product_id)

    def create_raw_data_folder(self):
        dir = os.path.join("C:\\", "Users\\victo\\AiCoreCoursework\\data-collection-pipeline", "raw_data")
        if not os.path.exists(dir):
            os.mkdir(dir)

    def create_id_subfolder(self):
        subdir = os.path.join("C:\\", "Users\\victo\\AiCoreCoursework\\data-collection-pipeline\\raw_data", self.product_id)
        if not os.path.exists(subdir):
            os.mkdir(subdir)

    def save_image(self): # downloads image and saves it in images folder
        img_dir = os.path.join("C:\\", f"Users\\victo\\AiCoreCoursework\\data-collection-pipeline\\raw_data\\{self.product_id}", "images")
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)
        
        image_url_list = self.dict_products['Image']
        image_url = image_url_list[0]
        img_data = requests.get(image_url).content
        
        with open(f'raw_data\\{self.product_id}\\images\\Product Image.jpg', 'wb') as handler:
            handler.write(img_data)

    def dump_data(self):
        self.create_raw_data_folder()
        self.create_id_subfolder()
        with open(f'raw_data\\{self.product_id}\\json_data.json', 'w') as f:
            json.dump(self.dict_products, f, indent=6)
        self.save_image()
         
        
def do_scrape():
    new_scraper = Scraper()
    new_scraper.get_image()
    new_scraper.get_text()
    new_scraper.get_timestamp()
    new_scraper.get_id()
    new_scraper.dump_data()
    
if __name__ == "__main__":
    do_scrape()