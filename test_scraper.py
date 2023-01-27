from scraper import Scraper
from selenium.webdriver.common.by import By
import unittest
import unittest.mock as mock
import time

class Dpl_mainTestCase(unittest.TestCase):
    
    def setUp(self):
        self.scraper = Scraper('https://www.ocado.com/search?entry=frubes')
        self.product_page = 'https://www.ocado.com/products/frubes-strawberry-yoghurt-30542011'
        self.scraper.initialise_dictionary()

    def open_product_page(self):
        self.scraper.driver.get(self.product_page)
        time.sleep(1)
        self.scraper.accept_cookies()
        time.sleep(1)

    def test_create_product_url_list(self, expected = 3):
        url_list = self.scraper.create_product_url_list()
        self.assertIs(type(url_list), list)
        self.assertEqual(expected, len(self.scraper.product_url_list))

    def test_get_image_url(self):
        self.open_product_page()
        self.scraper.get_image_url()
        self.assertEqual("https://www.ocado.com/productImages/305/30542011_0_640x640.jpg?identifier=26128dc4f17d53769f81417b59c54201", self.scraper.image_src)

    def test_get_text(self):
        self.open_product_page()
        self.scraper.get_text()
        self.assertEqual("Frubes Strawberry Yoghurt 9 x 37g", self.scraper.product_name)
        self.assertEqual("45.1p per 100g", self.scraper.price)
        self.assertEqual("Good Stuff inside\n...and cool stuff on the back", self.scraper.description)
        self.assertEqual("4.5", self.scraper.rating)

    def test_get_product_id(self):
        '''test for 8-digit ID number'''
        self.scraper.product_url = 'https://www.ocado.com/products/frubes-strawberry-yoghurt-30542011'
        self.scraper.driver.get(self.scraper.product_url)
        time.sleep(1)
        self.scraper.accept_cookies()
        time.sleep(1)
        self.scraper.get_product_id()
        self.assertEqual("30542011", self.scraper.product_id)
        '''test for 9-digit ID number'''
        self.scraper.product_url = 'https://www.ocado.com/products/frubes-strawberry-banana-flavour-yoghurt-259279011'
        self.scraper.driver.get(self.scraper.product_url)
        time.sleep(1)
        self.scraper.accept_cookies()
        time.sleep(1)
        self.scraper.get_product_id()
        self.assertEqual("259279011", self.scraper.product_id)

    def test_create_dictionary(self):
        self.scraper.product_url = 'https://www.ocado.com/products/frubes-strawberry-yoghurt-30542011'
        self.scraper.driver.get(self.scraper.product_url)
        time.sleep(1)
        self.scraper.accept_cookies()
        time.sleep(1)
        self.scraper.get_image_url()
        self.scraper.get_text()
        self.scraper.get_timestamp()
        self.scraper.get_product_id()
       
        expected_dictionary = {
            'Image': ['https://www.ocado.com/productImages/305/30542011_0_640x640.jpg?identifier=26128dc4f17d53769f81417b59c54201'], 
            'Product Name': ['Frubes Strawberry Yoghurt 9 x 37g'], 
            'Price': ['45.1p per 100g'], 
            'Description': ['Good Stuff inside\n...and cool stuff on the back'], 
            'Rating': ['4.5'], 
            'Timestamp': [mock.ANY], 
            'ID': ['30542011']}
        self.assertEqual(expected_dictionary, self.scraper.dict_products)

    def tearDown(self):
        self.scraper.driver.close()

if __name__ == '__main__':
    unittest.main()