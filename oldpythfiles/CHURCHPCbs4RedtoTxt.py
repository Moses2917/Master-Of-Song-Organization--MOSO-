from html import parser
import time, os.path, bs4, requests
from xml.etree.ElementInclude import include
from time import sleep
from bs4 import BeautifulSoup
bs4.BeautifulSoup()
songNum = 750
webpage = r"http://www.ergaran.in/2018/07/" + str(songNum) + ".html"
reqs = requests.get(webpage)
borsht = BeautifulSoup(reqs.content.decode('utf-8'), "lxml")
# print(borsht.prettify())
texts = borsht.find(class_ = 'post-body entry-content').get_text(" \n ", strip=False)
print(str(songNum) + "\n" + texts)
ntext = ""
rangeInts = range(len(texts))

for i in rangeInts:
    if (rangeInts[i] - i) < 0 or (rangeInts[i] - i+1) < 0 or (rangeInts[i] - i+2) < 0:
        if(rangeInts[i] - i) < 0 or (rangeInts[i] - i+1) < 0:
            iii = texts[i] + texts[i+1]
            if (rangeInts[i] - i) < 0:
                break
    else:
        
        iii = texts[i] + texts[i+1] + texts[i+2]
    if("\n \n" in iii and not("\n \xa0" in iii)):
        ntext += ""
    else:
        ntext += iii
    i += 3


# filtered = filter(lambda x: not re.match(r'^\s*$', x), original)
# print(borsht.find(class_ = 'post hentry uncustomized-post-template').get_text(" \n ", strip=False).strip()) ## it works!!!

print(str(songNum) + "\n" + ntext)
# print(str(songNum)+"\n"+ texts.replace("\n"," "))

failedSongs = [] ##if /n and not /xa0

while songNum < 661:
    try:
        webpage = r"http://www.ergaran.in/2016/01/" + str(songNum) + ".html"
        reqs = requests.get(webpage)
        borsht = BeautifulSoup(reqs.content.decode('utf-8'), 'html.parser')
        f = open("D:/Ergaran Web Word Songs/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
        print(borsht.find(class_ = 'post hentry uncustomized-post-template').get_text(" \n ", strip=True)) ## it works!!!
        text = borsht.find(class_ = 'post hentry uncustomized-post-template').get_text(" \n ", strip=True)
        f.write(text)
        f.close
    except:
        print("Did not find: " + str(songNum))
        failedSongs.append(songNum)
    songNum += 1


while songNum < 941:
    try:
        webpage = r"http://www.ergaran.in/2018/07/" + str(songNum) + ".html"
        reqs = requests.get(webpage)
        borsht = BeautifulSoup(reqs.content.decode('utf-8'), 'html.parser')
        f = open("D:/Ergaran Web Word Songs/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
        print(borsht.find(class_ = 'post hentry uncustomized-post-template').get_text(" \n ", strip=True)) ## it works!!!
        text = borsht.find(class_ = 'post hentry uncustomized-post-template').get_text(" \n ", strip=True)
        f.write(text)
        f.close
    except:
        print("Did not find: " + str(songNum))
        failedSongs.append(songNum)
    songNum += 1

while songNum < 1000:
    try:
        webpage = r"http://www.ergaran.in/2018/08/" + str(songNum) + ".html"
        reqs = requests.get(webpage)
        borsht = BeautifulSoup(reqs.content.decode('utf-8'), 'html.parser')
        f = open("D:/Ergaran Web Word Songs/"+ str(songNum) + ".txt", 'w', encoding='utf_8')
        print(borsht.find(class_ = 'post hentry uncustomized-post-template').get_text(" \n ", strip=True)) ## it works!!!
        text = borsht.find(class_ = 'post hentry uncustomized-post-template').get_text(" \n ", strip=True)
        f.write(text)
        f.close
    except:
        print("Did not find: " + str(songNum))
        failedSongs.append(songNum)
    songNum += 1

f = open("D:/Ergaran Web Word Songs/"+ "failedSongs" + ".txt", 'w', encoding='utf_8')
for x in failedSongs:
    print(x)
    f.write(str(x))
f.close


##    sleep(0.1)


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
