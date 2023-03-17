import time
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


import os.path
import docx


option = webdriver.ChromeOptions()
option.add_argument('headless') ##For running it in headless mode, not needed in early stages of development
# driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

##songNum = 1
songNum = 1
failedSongs = []


while songNum <= 658:
    webpage = r"http://www.ergaran.in/2016/01/" + str(songNum) + ".html"
    try:
        print(driver.find_element("post.hentry.uncustomized-post-template").text)
    except:
        print(str(songNum)+":Does not exsist at, " + webpage)
        failedSongs.append(songNum)
        songNum +=1
        
driver.quit()


# WORKS DO NOT MOVE
# while True:
#     try:
#         ##PLAN iterate through all songs from 1-1000, by constantly changing  the url, by adding one
#         ##Using full thing ---- post hentry uncustomized-post-template---THIS IS BETTER
#         webpage = r"http://www.ergaran.in/2016/01/" + str(songNum) + ".html" # edit me
#         ##driver = webdriver.Chrome()
#         driver.get(webpage)
#         sleep(0.5)
#         ##print(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text) ##Finds full text for song, with song num.
#         print("(OLD)On song number: " + str(songNum))
#         f = open("M:/word/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
#         f.write(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text)
#         f.close()

        
#     except:
#         failedSongs.append(songNum)
#     songNum +=1



while songNum > 658:
    
    # try:
    #     ##PLAN iterate through all songs from 1-1000, by constantly changing  the url, by adding one
    #     ##Using full thing ---- post hentry uncustomized-post-template---THIS IS BETTER
    #     webpage = r"http://www.ergaran.in/2018/07/" + str(songNum) + ".html" # edit me
    #     ##driver = webdriver.Chrome()
    #     driver.get(webpage)
    #     sleep(0.5)
    #     ##print(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text) ##Finds full text for song, with song num.
    #     print("(WTF)On song number: " + str(songNum))
    #     f = open("M:/newWord/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
    #     # print("this is the song text: \n" + driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text)
    #     # f.write(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text)
    #     print(driver.find_element(By.ID, 'post-body.entry-content'))
    #     # f.write(driver.find_element(By.CLASS_NAME, 'post.hentry.uncustomized-post-template'))
    #     f.close()

        
    # except:
    #     failedSongs.append(songNum)
    #     f.write("FAILED")

    ##PLAN iterate through all songs from 1-1000, by constantly changing  the url, by adding one
    ##Using full thing ---- post hentry uncustomized-post-template---THIS IS BETTER
    webpage = r"http://www.ergaran.in/2018/07/" + str(songNum) + ".html" # edit me
    ##driver = webdriver.Chrome()
    driver.get(webpage)
    sleep(0.55)
    ##print(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text) ##Finds full text for song, with song num.
    print("(WTF)On song number: " + str(songNum))
    f = open("M:/newWord/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
    # print("this is the song text: \n" + driver.find_element('class name', ".post.hentry.uncustomized-post-template").text)
    print("this is the song text: \n" + driver.find_element(By.CLASS_NAME, 'post hentry uncustomized-post-template').text)
    # f.write(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text)
    # f.write(driver.find_element(By.CLASS_NAME, 'post.hentry.uncustomized-post-template'))
    f.close()

    

    failedSongs.append(songNum)
    f.write("FAILED")
    songNum +=1
        
while songNum > 939 and songNum <= 1000:
        try:
            ##PLAN iterate through all songs from 1-1000, by constantly changing  the url, by adding one
            ##Using full thing ---- post hentry uncustomized-post-template---THIS IS BETTER
            webpage = r"http://www.ergaran.in/2018/08/" + str(songNum) + ".html" # edit me
            ##driver = webdriver.Chrome()
            driver.get(webpage)
            sleep(0.5)
            ##print(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text) ##Finds full text for song, with song num.
            print("On song number: " + str(songNum))
            f = open("M:/newWord/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
            f.write(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text)
            f.close()

            
        except:
            failedSongs.append(songNum)
            
        songNum +=1
    


##failedSongs = redToWord(songNum, failedSongs, driver)

##failedSongs = errors(songNum, failedSongs, driver)

failed = open("M:/newWord/FailedSongs.txt",'w', encoding='utf_8')
for x in failedSongs:
    failed.write(str(x) + ", ")
failed.close()

driver.quit()

##-------------------------Archived Code Purly for just in case Senario--------------------

##                  Using the post-body entry

##while songNum <= 1000:
##    ##PLAN iterate through all songs from 1-1000, by constantly changing  the url, by adding one
##
##    webpage = r"http://www.ergaran.in/2016/01/" + str(songNum) + ".html" # edit me
##    ##driver = webdriver.Chrome()
##    driver.get(webpage)
##    sleep(1)
##    print(driver.find_element_by_class_name("post-body.entry-content").text) ##Finds full text for song, without song num in it :(
##    songNum += 1



#def redToWord(songNum, failedSongs, driver):
#
#    while songNum <= 660:
#        try:
#            ##PLAN iterate through all songs from 1-1000, by constantly changing  the url, by adding one
#            ##Using full thing ---- post hentry uncustomized-post-template---THIS IS BETTER
#            webpage = r"http://www.ergaran.in/2016/01/" + str(songNum) + ".html" # edit me
#            ##driver = webdriver.Chrome()
#            driver.get(webpage)
#            sleep(0.5)
#            ##print(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text) ##Finds full text for song, with song num.
#            print("On song number: " + str(songNum))
#            f = open("M:/word/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
#            f.write(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text)
#            f.close()
#
#            
#        except:
#            
#            try:
#                webpage =  r"http://www.ergaran.in/2016/01/0" + str(songNum) + ".html"
#                f = open("M:/word/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
#                f.write(driver.find_element_by_class_name("post.hentry.uncustomized-post-template").text)
#                f.close()
#                print(str(songNum) + " Found"
#            except:
#                
#                failedSongs.append(songNum)
#                
#        songNum +=1
#        return null