from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import json
import os
import requests
import time

class Scraper():
    def __init__(self, url):
        self.driver = webdriver.Firefox()
        path = '/Users/victo/Drivers/geckodriver.exe'
        self.url_to_scrape = url
        self.dict_products = {'Image': [], 'Product Name': [], 'Price': [], 'Description': [], 'Rating': [], 'Timestamp': [], 'ID': []}

    def accept_cookies(self):
        '''
        This method accepts the cookies by clicking on the button if displayed.
        '''
        try:
            accept_cookies_button = self.driver.find_element(by=By.ID, value='onetrust-accept-btn-handler')
            accept_cookies_button.click()
            
        except AttributeError: 
            accept_cookies_button = self.driver.find_element(by=By.ID, value='onetrust-accept-btn-handler')
            accept_cookies_button.click()

        except:
            pass 
    
    def open_results_page(self):
        '''
        This method opens a page of products; maximises the browser to fit more products on the page; and calls scroll_down_all to reveal all the products.
        '''
        self.driver.maximize_window()
        self.driver.get(self.url_to_scrape)
        time.sleep(2)
        self.accept_cookies()
        time.sleep(1)
        self.scroll_down_all()
    
    def scroll_down_all(self): 
        '''
        If there more products than fit in the browser window, you need to keeping scrolling down to the bottom of the page to reveal them all. 
        This method performs that task, by alternately scolling and pausing to give the system time to load the results.
        '''
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(1, last_height, 1000):
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, {});".format(i))

    def create_product_url_list(self):
        '''
        This method finds the URL of the individual product page for each search result.
        This also adds three recommended products that we don't want to scrape data for, so these are removed from the list.
        '''
        self.open_results_page()
        product_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="fop-contentWrapper"]')
        url_list_including_recommended_products = []

        for product in product_container:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute("href")
            url_list_including_recommended_products.append(link)
        self.product_url_list = url_list_including_recommended_products[3:]
        print(self.product_url_list)
        print(f'There are {len(self.product_url_list)} products on this page.')
        return self.product_url_list

    def get_image_url(self):
        '''
        This method finds the source URL of the product image and adds it to the dictionary.
        ''' 
        print('Getting image URL')
        image_container = self.driver.find_element(by=By.XPATH, value='//img[@class="bop-gallery__image"]')
        self.image_src = image_container.get_attribute("src")
        self.dict_products['Image'].append(self.image_src)

    def get_text(self):
        '''
        This method finds the name of the product (including volume), the price, the description text and the customer rating (if it has one), and adds them to the dictionary.
        '''
        print('Scraping text')
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
        '''
        This method adds a timestamp of when the data was scraped to the dictionary.
        '''
        print('Getting timestamp')
        self.timestamp = datetime.datetime.now()
        self.dict_products['Timestamp'].append(self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    def get_product_id(self):
        '''
        This method finds the product ID number, by taking it from the end of the product page URL, and adds it to the dictionary.
        '''
        print('Getting Product ID')
        product_id_with_hyphen = self.product_url[-9:]
        if '-' in product_id_with_hyphen:
            self.product_id = product_id_with_hyphen.replace('-','')
        else:
            self.product_id = product_id_with_hyphen
        self.dict_products['ID'].append(self.product_id)

    def create_raw_data_folder(self):
        '''
        This method creates a folder named "raw_data" if it doesn't already exist.
        '''
        dir = os.path.join("C:\\", "Users\\victo\\AiCoreCoursework\\data-collection-pipeline", "raw_data")
        if not os.path.exists(dir):
            os.mkdir(dir)
            print('Creating raw data folder')
        else:
            print('Raw data folder already exists!')
    
    def create_id_subfolder(self):
        '''
        This method creates a subfolder in the "raw_data" folder, with the product ID number as its name.
        '''
        subdir = os.path.join("C:\\", "Users\\victo\\AiCoreCoursework\\data-collection-pipeline\\raw_data", self.product_id)
        if not os.path.exists(subdir):
            os.mkdir(subdir)
            print('Creating ID folder')
        else:
            print('ID folder already exists!')

    def save_image(self): 
        '''
        This method creates a subfolder named "images" in the product ID folder. Then it downloads the product image jpeg from the source URL and saves it in the "images" folder.
        '''
        img_dir = os.path.join("C:\\", f"Users\\victo\\AiCoreCoursework\\data-collection-pipeline\\raw_data\\{self.product_id}", "images")
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)
            print('Creating images folder')
        
        image_url_list = self.dict_products['Image']
        image_url = image_url_list[0]
        img_data = requests.get(image_url).content
        
        with open(f'raw_data\\{self.product_id}\\images\\Product Image.jpg', 'wb') as handler:
            handler.write(img_data)
        print('Product image saved in images folder')

    def save_dictionary_to_json_file(self):
        '''
        This method saves the dictionary in a json file and stores it in the product id subfolder.
        '''
        self.create_raw_data_folder()
        self.create_id_subfolder()
        with open(f'raw_data\\{self.product_id}\\json_data.json', 'w') as f:
            json.dump(self.dict_products, f, indent=6)
        self.save_image()
        print('Saving dictionary in json file')

    def open_product_page(self):
        '''
        This method begins the web scraping process. It calls the method that creates a list of product page urls. 
        It then opens each page and scrapes the data.
        '''
        self.create_product_url_list()

        for self.product_url in self.product_url_list:
            self.driver.get(self.product_url)
            self.scrape_data()
        
    def scrape_data(self):
        '''
        This function calls all the methods to collect and store the data and image.
        '''
        self.get_image_url()
        self.get_text()
        self.get_timestamp()
        self.get_product_id()
        self.save_dictionary_to_json_file()
    
    
def scrape_all():
    new_scraper = Scraper('https://www.ocado.com/search?entry=frubes')
    new_scraper.open_product_page()
    new_scraper.driver.close()
    
if __name__ == "__main__":
    scrape_all()
    