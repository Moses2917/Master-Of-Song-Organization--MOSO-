import time

import bs4
import requests
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

webpage = r"https://www.jaser-services.com/blank-2"
option = webdriver.ChromeOptions()
# option.add_argument('headless') ##For running it in headless mode, not needed in early stages of development
# driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get(webpage)
open(r"mac/Top Names.txt")

name = "Grigor"
email = "wedosome@trolling" ##make one of them "andrew loves men"
address = "your mom's house"
message = "Hi I would like to inquire about your services"
##Have it loop through
# reqs = requests.get(webpage)
# borsht = BeautifulSoup(reqs.content.decode('utf-8'), "lxml")
# print(borsht.find(id="input_comp-l9j52qze2"))
sbox = driver.find_element(By.ID, "input_comp-l9j52qze2")
print(sbox)
sbox.clear()
# ActionChains.send_keys_to_element(driver.find_element(By.ID, "input_comp-l9j52qze2"), 'v')
sbox.send_keys(name)
ebox = driver.find_element(By.ID, "input_comp-l9j52qzg3")
sbox.clear()
sbox.send_keys(email)