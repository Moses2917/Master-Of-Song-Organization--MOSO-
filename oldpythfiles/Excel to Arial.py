from time import sleep
import pyautogui
from pyautogui import scroll
from pyautogui import press
from pyautogui import hotkey, keyDown, keyUp
import selenium
from selenium import webdriver
import itertools
from itertools import repeat


webpage = r"http://www.armdict.com/tool/unicode-converter/" # edit me
driver = webdriver.Chrome()
driver.get(webpage)

def translateAM():
    ##Goto first box
    sbox = driver.find_element_by_id("convertr_box") # Finds first box
    sleep(0.5)
    sbox.clear()
    #pyautogui.hotkey('ctrl', 'v')  # ctrl-v to paste # the searchterm
    sbox.WebElement.ActionChains.key_down(Keys.CONTROL).send_keys('v')
    #sbox.send_keys("11  ÊáñÑñ¹³íáñ ¿ ³Ûë Ñ³Ý¹»ë")
    sleep(1)
    sbox.click()

    #Goto Second box
    obox = driver.find_element_by_xpath('//*[@id="convertr_box"]')
    ##obox.click()
    ##Arial = obox.text
    ##print(Arial)
    obox.send_keys()
    
    sleep(0.5)
    ##pyautogui.hotkey('ctrl', 'a')
    ##pyautogui.hotkey('ctrl', 'c')
    sleep(0.5)



translateAM()
