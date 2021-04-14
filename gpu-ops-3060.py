from selenium import webdriver
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request
from datetime import datetime
import time
from random import randint
import winsound


def scrape_site(url):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return soup

def time_delay():
    num = randint(1,3)
    time.sleep(num)
    
def alert():
    duration = 5000  # milliseconds
    freq = 4000  # Hz
    sound = winsound.Beep(freq, duration)
    return sound

def main():
    url = 'https://www.bestbuy.com/site/evga-nvidia-geforce-rtx-3060-xc-gaming-12gb-gddr6-pci-express-4-0-graphics-card/6454328.p?skuId=6454328'
    attempt = 0
    out_of_stock = True
    message = 'sold out'
    
    while out_of_stock:
        scraped_site = scrape_site(url)
        button_status = scraped_site.find_all(class_='add-to-cart-button')[0].get_text()
        attempt += 1
        
        if button_status.lower() == message:
            # Out of stock
            print(f'Time: {datetime.now()}. Attempt: {attempt}')
            time_delay()
        
        if button_status.lower() != message:
            # No longer out of stock!
            print('Item no longer Coming Soon!')
            alert()
            out_of_stock = False
        
main()