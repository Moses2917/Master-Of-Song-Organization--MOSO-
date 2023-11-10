import json, re, docx
from glob import glob
# f=open("redsongs.json", 'r', encoding='utf-8')
# file = json.load(f)
# # print(file)
# f.close()
#Note: think of a json as a multi-array such as [][][]

def process(filename):
    text = ""
    doc = docx.Document(filename)
    for p in doc.paragraphs:
        text += p.text + "\n"
    title = re.findall("\n(\d.*)\n",text)
    return title[0]

versionNum = 1
RedDir = glob("C:/Users/moses/OneDrive/Word songs/*.docx")
g = open("redsongsexample.json", 'r', encoding='utf-8')
file = json.load(g)
g.close()
g = open("wordSongsIndex.json", 'w', encoding='utf-8')
# g.write("{}")
# file = json.load(g)
file['SongNum'] = {}
for song in RedDir:
    
    try:
        songNum =  str(re.findall(r'\d+',song)[0])
    except:
        songNum = ""

    try:
        # title = process(song)
        title = re.findall(r'(?<=\\)\d+\s(.+?)(?=\.)',song)[0] # Good for songs from ergaran/red book
    except:
        title = ""

    file['SongNum'][songNum] = {} #create a directory with that song number
    file['SongNum'][songNum]["Title"] = title        
    file['SongNum'][songNum]["latestVersion"] = "Word songs/" + songNum + " " + title + ".docx" #stores current location of this version of the file
    file['SongNum'][songNum]["v" + str(versionNum)] = "Word songs/" + songNum + " " + title + ".docx" #stores current location of this version of the file
    
    
json.dump(file, g, indent=4, ensure_ascii=False)














def ergaran():
    versionNum = 1
    ErgerDir = glob("C:/Users/moses/OneDrive/Երգարան Word Files/*.docx")
    g = open("ergaran.json", 'r', encoding='utf-8')
    file = json.load(g)
    g.close()
    g = open("ergaran.json", 'w', encoding='utf-8')
    file['SongNum'] = {}
    for song in ErgerDir:
        songNum =  str(re.findall(r'\d+',song)[0])
        try:
            title = re.findall(r'(?<=\\)\d+\s(.+?)(?=\.)',song)[0]
        except:
            title = ""
        file['SongNum'][songNum] = {} #create a directory with that song number
        file['SongNum'][songNum]["Title"] = title        
        file['SongNum'][songNum]["latestVersion"] = "Երգարան Word Files/" + songNum + " " + title + ".docx" #stores current location of this version of the file
        file['SongNum'][songNum]["v" + str(versionNum)] = "Երգարան Word Files/" + songNum + " " + title + ".docx" #stores current location of this version of the file
        
        
    json.dump(file, g, indent=4, ensure_ascii=False)

def findSong():
    f = open("ergaran.json", 'r', encoding='utf-8')
    ergaran = json.load(f)
    f.close

    x = "125"

    for songNum in ergaran["SongNum"]:
        if songNum == x:
                filename = ergaran["SongNum"][x]["latestVersion"]
                print(filename)
                exit()