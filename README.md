# Data Collection Pipeline
An implementation of an industry grade data collection pipeline that runs scalably in the cloud. 
This project forms part of my coursework for the AiCore Data Analytics course. The final scraper file is scraper.py.

## Milestones 1-3
I chose to scrape data for products on the Ocado website, as this is a search I often perform and I am familiar with the site.

I have used Selenium Webdriver as my selected website includes Javascript, and I am using Firefox as a browser, so I need geckodriver to use this with Selenium.

The code for these milestones is in dpl_main.py. The Scraper class opens the chosen website, maximises the browser and compiles a list of all product page URLs, scrolling down the page to reveal all the results.

## Milestone 4
This code (milestone_4.py) performs a web scrape on a single product on the Ocado website. It collects the following data:
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

## Milestone 5
The code in dpl_main.py and milestone_4.py has been combined in scraper.py. This compiles a list of product page URLs and opens each one to scrape the text and image from each one. I have used a page with only three product results for now, so that testing the code is faster and won't result in a large quantity of data being saved on my hard drive. 

test_scraper.py contains unit tests for the main methods in the Scraper class.
I have imported unittest to perform the tests.

## Milestones 6 & 7
In these milestones, I corrected some errors in my code and updated scraper.py and test_scraper.py.
I have updated the scraper to perform a web scrape on a larger number of products and it now runs in headless mode. 
I have containerised the scraper using Docker and deployed the image to DockerHub.
I have set up a CI/CD pipeline using GitHub Actions, so that the Docker image is built whenever an update is pushed to the GitHub repository.

