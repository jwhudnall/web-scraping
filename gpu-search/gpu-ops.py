from selenium import webdriver
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request
from datetime import datetime
import time
from random import randint
import winsound

# Chrome Version
# 4/3/2021
# Version 89.0.4389.114 (Official Build) (64-bit)

def scrape_site(url):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return soup

def time_delay():
    num = randint(2,5)
    time.sleep(num)
    
def alert():
    duration = 5000  # milliseconds
    freq = 4000  # Hz
    sound = winsound.Beep(freq, duration)
    return sound

def main():
    url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'
    attempt = 0
    out_of_stock = True
    
    while out_of_stock:
        scraped_site = scrape_site(url)
        button_status = scraped_site.find_all(class_='add-to-cart-button')[0].get_text()
        attempt += 1
        
        if button_status.lower() == 'sold out':
            # Out of stock
            print(f'Time: {datetime.now()}. Attempt: {attempt}')
            time_delay()
        
        if button_status.lower() != 'sold out':
            # No longer out of stock!
            print('Item no longer out of stock!')
            alert()
            out_of_stock = False
        
main()