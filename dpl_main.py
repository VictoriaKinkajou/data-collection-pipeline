from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

class Scraper():
    def __init__(self):
        self.driver = webdriver.Firefox()
        path = '/Users/victo/Drivers/geckodriver.exe'

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
        self.driver.get("https://www.ocado.com/browse/beer-wine-spirits-43510/wine-135827/red-wine-45710/shop-by-country-319550/france-45724")
        time.sleep(2)
        self.accept_cookies()
        time.sleep(1)
        self.scroll_down_all()
    
    def scroll_down_all(self): #scrolls down the page of results to reveal next section of results

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(1, last_height, 1000):
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, {});".format(i))

    def get_links(self):
        self.open_shelf()
        product_list = self.driver.find_elements(by=By.XPATH, value='//div[@class="fop-contentWrapper"]')
        self.link_list = []

        for product in product_list:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute("href")
            self.link_list.append(link)
        print(self.link_list)
        print(f'There are {len(self.link_list)} products on this page.')
        
def print_list_of_links():
    new_scraper = Scraper()
    new_scraper.get_links()
    
if __name__ == "__main__":
    print_list_of_links()