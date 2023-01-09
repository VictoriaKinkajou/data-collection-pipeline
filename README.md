# Data Collection Pipeline
An implementation of an industry grade data collection pipeline that runs scalably in the cloud. 

## Milestones 1-3
I chose to scrape data for french red wine on the Ocado website, as this is a search I often perform and I am familiar with the site.

I have used Selenium Webdriver as my selected website includes Javascript.

The code for these milestones is in dpl_mail.py. The Scraper class opens the chosen website, maximises the browser and compiles a list of all product page URLs, scrolling down the page to reveal all the results.

## Milestone 4
This code performs a web scrape on a single product on the Ocado website. It collects the following data:
  - Product Name
  - Price
  - Image URL
  - Description
  - Customer rating
  - Timestamp of when data was scraped
  - Product ID number
The data is stored as a dictionary in a json file.
A directory named with the product ID number is created, in which the json file is stored. 
The product image jpeg is downloaded and stored in a subdirectory named 'images'.

I have imported the following modules:
  - Selenium Webdriver to perform the web scrape
  - time to add pauses to the code in order for web pages to fully load
  - datetime to create the timestamp
  - os to create and manage directories
  - requests to download the image
  - json to save the dictionary
