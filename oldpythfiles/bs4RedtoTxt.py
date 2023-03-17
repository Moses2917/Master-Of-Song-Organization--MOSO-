from html import parser
import time, os.path, bs4, requests
from xml.etree.ElementInclude import include
from time import sleep
from bs4 import BeautifulSoup
bs4.BeautifulSoup()
songNum = 661
webpage = r"http://www.ergaran.in/2018/07/" + str(songNum) + ".html" 
reqs = requests.get(webpage)
borsht = BeautifulSoup(reqs.text, "lxml")
# print(borsht.prettify())
# print(borsht.find_all(class_ = "post-body entry-content").get_text(" \n ", strip=True)) ## it works!!!
txt = str(songNum)
txt += borsht.find(class_ = "post-body entry-content").get_text("")
print(txt) ## it works!!!
songNum = 672
webpage = r"http://www.ergaran.in/2018/07/" + str(songNum) + ".html" 
reqs = requests.get(webpage)
borsht = BeautifulSoup(reqs.text, "lxml")
txt2 = str(songNum)
txt2 += borsht.find(class_ = "post-body entry-content").get_text("")
print(txt2)


# if index - 1 is not \n go back and reGET but with get_text("\n"), or just set index-1 = "\n"
for x in str(txt2):
    print()

# failedSongs = []

# while songNum < 659: ## 2016/01/
#     webpage = r"http://www.ergaran.in/2016/01/" + str(songNum) + ".html"
#     try:
#         reqs = requests.get(webpage)
#         sleep(0.5)
#         borsht = BeautifulSoup(reqs.content, "html.parser")
#         text = borsht.find(class_ = 'post hentry uncustomized-post-template').text
#         print(text) ## it works!!!
#         f = open("M:/newWord/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
#         sleep(0.5)
#         f.write(text)
#         f.close
#     except:
#         failedSongs.append(songNum)
#     songNum += 1

# while songNum < 941: ## 2018/07/
#     webpage = r"http://www.ergaran.in/2018/07/" + str(songNum) + ".html"
#     try:
#         reqs = requests.get(webpage)
#         sleep(0.5)
#         borsht = BeautifulSoup(reqs.content, "html.parser")
#         text = borsht.find(class_ = 'post hentry uncustomized-post-template').text
#         print(text) ## it works!!!
#         f = open("M:/newWord/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
#         sleep(0.5)
#         f.write(text)
#         f.close
#     except:
#         failedSongs.append(songNum)
#     songNum += 1

# while songNum < 1001: ## 2018/08/
#     webpage = r"http://www.ergaran.in/2018/08/" + str(songNum) + ".html"
#     try:
#         reqs = requests.get(webpage)
#         sleep(0.5)
#         borsht = BeautifulSoup(reqs.content, "html.parser")
#         text = borsht.find(class_ = 'post hentry uncustomized-post-template').text
#         print(text) ## it works!!!
#         f = open("M:/newWord/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
#         sleep(0.5)
#         f.write(text)
#         f.close
#     except:
#         failedSongs.append(songNum)
#     songNum += 1
