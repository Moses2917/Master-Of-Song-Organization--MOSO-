import re, time, docx, json
from os import path as pth, remove
from docx.shared import Pt

month = time.strftime('%m')
year = time.strftime('%y')
fullYear = time.strftime('%Y')
day = time.strftime('%d')

def getDocText(filename):
    text = ""

    doc = docx.Document(filename)
    for p in doc.paragraphs:
        text += p.text + "\n"
    return text
def getOldSongTitle(oldSong_text):
    tab = re.findall("\n.+", oldSong_text) # for finding title
    # print(tab[1])
    title = tab[1]
    # Use re.sub() to remove "1." and "," from the text
    title = re.sub(r"1.", "", title)
    title = re.sub(r",", "", title)
    title = re.sub(r"\n", "", title)
    print(title)
    return title
#gets first line of song and uses that as title
def getRedSongTitle(text):
    return re.findall("\n(\d.*)\n",text)[0] 
#Finds the biggest version and returns it as an int
def findLatestVer(file,song_num):
    # filename = file["SongNum"][str(song_num)]["latestVersion"] = "Word songs/" + str(song_num) + " " + title + ".docx"
    song_params = file['SongNum'][song_num]
    # verList = re.findall("v*",str(file['SongNum'][song_num])) #problem, can't rly run a findall on a json dict/list
    biggest = 0
    for param in song_params:
        if "v" in param:
            #check for biggest version
            ver = re.findall("\d",param)[0]
            if int(ver) > int(biggest):
                biggest = ver
    return int(biggest)
    #Also also I could find the file loc of latest version and just add one.
def getDocTextAndIndentation(filename:str):
    doc = docx.Document(filename)
    text_and_indentation = [] #turn into a list of lists
    song = []
    bookOld = False
    for p in doc.paragraphs:
        if "[start:song" in p.text:
            song = []
            if "old" in p.text:
                bookOld = True
        if not("end" in p.text or "start" in p.text):
            first_line_indent = p.paragraph_format.first_line_indent
            left_indent = p.paragraph_format.left_indent
            right_indent = p.paragraph_format.right_indent
            song.append({
                'text': p.text,
                # 'book': re.findall(pattern, p.text,re.DOTALL)[0],
                # 'old': bookOld,
                'first_line_indent': first_line_indent,
                'left_indent': left_indent,
                'right_indent': right_indent
            })
        if "end" in p.text:
            #push song to text var and reset song var
            text_and_indentation.append({
                'song': song,
                'book': bookOld
            })
            bookOld = False
            song = []
    return text_and_indentation
def FindNum(song):
    return (re.findall("\d+",song[0]['text']))[0] #+ str(song[0]['old'])
#Function that checks if the song is already in the index file & gets the song title:
def getSongTitle(input_filename, bookOld,song_num):
    #I know this method is not the fastest
    #won't work if the song is not in the index file
    #however, I can use this method to find the title of the song && check if the song is already in the index file 
    if bookOld:
        # with open(input_filename, 'r', encoding='utf-8') as f:
        #     fulltext = getDocText(input_filename)
        #     matches = re.findall("\[start:song(.*?)\[end:song]",fulltext,re.DOTALL)
        #     # return re.findall("\n(\d.*)\n",text)[0]
        #     return re.findall("\n(\d.*)\n",matches[song_num])[0]
        with open('wordSongsIndex.json', 'r') as json_file:
            data = json.load(json_file)
            if song_num in data['SongNum'][song_num]:
                return song_num + " already exists in songs.json"
            else:
                data.append(song_num)
                data.append()
        with open('songs.json', 'w') as json_file:
            json.dump(data, json_file)
        return song_num + " added to songs.json"
def getSongText(filename):
    song_doc = getDocText(filename)
    matches = []
    newMatches = re.findall("\[start:song](.*?)\[end:song]",song_doc,re.DOTALL)
    for match in newMatches:
        song_num = re.findall("\d+",match)[0] # for finding song num
        title = getRedSongTitle(match)
        matches.append({
            'song_num': song_num,
            'title': title,
            'text': match
        })
    oldMatches = re.findall("\[start:song:old](.*?)\[end:song:old]",song_doc,re.DOTALL)
    for oldMatch in oldMatches:
        song_num = re.findall("\d+",oldMatch)[0] # for finding song num
        title = getOldSongTitle(oldMatch)
        matches.append({
            'song_num': song_num,
            'title': title,
            'text': oldMatch
        })
        print(oldMatch)
    return matches # returns a list of all the songs in the file
def createDocFromTextAndIndentation(text_and_indentation):
    doc = docx.Document()
    word_doc = []
    for song in text_and_indentation:#gets one song out of the list of songs
        song_num = FindNum(song)
        oldBook = song[0]['old']
        for song_info in song:#gets on line out of all song lines
            p = doc.add_paragraph(song_info['text'])
            p.paragraph_format.space_after = 0
            if song_info['first_line_indent'] is not None:
                p.paragraph_format.first_line_indent = song_info['first_line_indent']
            if song_info['left_indent'] is not None:
                p.paragraph_format.left_indent = song_info['left_indent']
            if song_info['right_indent'] is not None:
                p.paragraph_format.right_indent = song_info['right_indent']
        #for loop ends here
        #call some odd function to sort out the title with json stuff
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(22)
        word_doc.append({
            'song_num': song_num,
            # 'title': title,
            'docx': doc,
            'old': oldBook #sets T or F, T=song is from old book
        })
        doc = docx.Document()

        # doc.save("D:/"+FindNum(song)+".docx")
    return word_doc

def saveDocFromTextAndIndentation(word_docs):
    for word_doc in word_docs:
        doc = word_doc['docx']
        oldBook = word_doc['old']
        song_num = word_doc['song_num']
        # title = word_doc['title']
        doc.save("D:/"+FindNum(song_num)+".docx")
        if oldBook:
            with open("wordSongsIndex.json", mode = 'r', encoding='utf-8') as f:
                file = json.load(f)
                if song_num in file['SongNum']:
                    file['SongNum'][song_num]["old"] = "F"
                else:
                    file['SongNum'][song_num]["old"] = "T"
            with open("wordSongsIndex.json", mode = 'w', encoding='utf-8') as f:
                json.dump(file, f, ensure_ascii=False, indent=4)
    
# def updateSong(user):
user = ""
if pth.exists("C:/Users/moses/"):
    user = "moses"
else:
    user = "Armne"

input_filename = '04.06.23.docx'
# getSongText("04.06.23.docx")
# getSongTitle(input_filename)
text_and_indentation = getDocTextAndIndentation(input_filename)
word_docs = createDocFromTextAndIndentation(text_and_indentation)
saveDocFromTextAndIndentation(word_docs)

# file={}
# f=open("wordSongsIndex.json", mode = 'r', encoding='utf-8')
# latestVer = findLatestVer(file,song_num) + 1 # should get back the latest version number
# saveFile = "C:/Users/" + user + "/OneDrive/Word songs/" + str(song_num) + " " + title + " v" + str(latestVer) + ".docx"
# try:
#     # file['SongNum'][song_num]["Title"] = title    
#     file['SongNum'][song_num]["latestVersion"] = saveFile #stores current location of this version of the file
    
#     file['SongNum'][song_num]["v" + str(latestVer)] = saveFile #stores current location of this version of the file
# except:
#     #if for some reason the song isn't already loged then this adds it
#     file['SongNum'][song_num] = {}
#     file['SongNum'][song_num]["Title"] = title        
#     file['SongNum'][song_num]["latestVersion"] = "Word songs/" + song_num + ".docx" #stores current location of this version of the file
#     file['SongNum'][song_num]["v1"] = "Word songs/" + song_num + ".docx" #stores current location of this version of the file
# with open("wordSongsIndex.json", mode="w",encoding="utf-8") as writeableFile:

#     json.dump(obj = file,fp=writeableFile, indent=4, ensure_ascii=False)










# Open the file and read its contents
# song_doc = getDocText("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + ".docx")
# song_doc = getDocText("C:/Users/Armne/OneDrive/Երգեր/04.2023/04.02.23.docx") 
# # Extract the songs from the document using regex

# # assuming the song_doc is the text you have provided
# matches = re.findall("\[start:song](.*?)\[end:song]",song_doc,re.DOTALL)

# for match in matches:
#     print(match)

# oldMatches = re.findall("\[start:song:old](.*?)\[end:song:old]",song_doc,re.DOTALL)

# for oldMatch in oldMatches:
#     print(oldMatch)

##Now its time to update the files!!!

def disabled():
    # Saves the newly updated red book songs in "Երգարան Word Files"
    with open("ergaran.json", mode = 'r', encoding='utf-8') as f:
        file = json.load(f)

    song_list = []
    for song_text in matches:
        song_num = re.findall("\d+",song_text)
        title = getRedSongTitle(song_text)
        # first_line = re.findall("\w   ",match) #First Line is being wack so I'm going to skip and start working with try
        print(song_num[0])
        doc = docx.Document("C:/Users/" + user + "/OneDrive/blankdoctemplate.docx")
        # style = doc.styles
        doc.add_paragraph(song_text)
        font = doc.styles['Normal'].font
        font.name = 'Arial'
        font.size = Pt(22)
        latestVer = findLatestVer(file,song_num) + 1 # should get back the latest version number
        saveFile = "C:/Users/" + user + "/OneDrive/Երգարան Word Files/" + str(song_num) + " " + title + " v" + str(latestVer) + ".docx"
        doc.save("C:/Users/" + user + "/OneDrive/Երգարան Word Files/" + str(song_num[0]) + title + ".docx") # Work on implimenting a Version Control System, can do smth like "165 V5 (n)" in MOSO



def disable():
    # Saves the newly updated old book songs in "Word Files", and notes it in index file
    f=open("wordSongsIndex.json", mode = 'r', encoding='utf-8')
    file = json.load(f)
    for oldSong_text in oldMatches:
        song_num = re.findall("\d+",oldSong_text)[0] # for finding som num
        title = getOldSongTitle(oldSong_text)
        print(song_num)
        # doc = docx.Document("C:/Users/" + user + "/OneDrive/blankdoctemplate.docx")
        # style = doc.styles
        # doc.add_paragraph(oldSong_text)
        # font = doc.styles['Normal'].font
        # font.name = 'Arial'
        # font.size = Pt(22)
        latestVer = findLatestVer(file,song_num) + 1 # should get back the latest version number
        saveFile = "C:/Users/" + user + "/OneDrive/Word songs/" + str(song_num) + " " + title + " v" + str(latestVer) + ".docx"
        # doc.save(saveFile)
        
        #Replace with checksong function
        try:
            # file['SongNum'][song_num]["Title"] = title    
            file['SongNum'][song_num]["latestVersion"] = saveFile #stores current location of this version of the file
            
            file['SongNum'][song_num]["v" + str(latestVer)] = saveFile #stores current location of this version of the file
        except:
            #if for some reason the song isn't already loged then this adds it
            file['SongNum'][song_num] = {}
            file['SongNum'][song_num]["Title"] = title        
            file['SongNum'][song_num]["latestVersion"] = "Word songs/" + song_num + ".docx" #stores current location of this version of the file
            file['SongNum'][song_num]["v1"] = "Word songs/" + song_num + ".docx" #stores current location of this version of the file

    with open("wordSongsIndex.json", mode="w",encoding="utf-8") as writeableFile:

        json.dump(obj = file,fp=writeableFile, indent=4, ensure_ascii=False)

