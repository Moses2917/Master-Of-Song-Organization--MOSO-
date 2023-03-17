import re
import time
import docx
from os import path as pth
from glob import glob
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
    print(tab[1])
    title = tab[1]
    # Use re.sub() to remove "1." and "," from the text
    title = re.sub(r"1.", "", title)
    title = re.sub(r",", "", title)
    title = re.sub(r"\n", "", title)
    print(title)
    return title

user = ""
if pth.exists("C:/Users/moses/"):
    user = "moses"
else:
    user = "Armne"

day = input("What day of this month needs updating, DD\n")

# Open the file and read its contents
song_doc = getDocText("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + ".docx")
# song_doc= getDocText("C:/Users/Armne/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + "13" + "." + year + ".docx")
# Extract the songs from the document using regex

# assuming the song_doc is the text you have provided
matches = re.findall("\[start:song](.*?)\[end:song]",song_doc,re.DOTALL)

for match in matches:
    print(match)

oldMatches = re.findall("\[start:song:old](.*?)\[end:song:old]",song_doc,re.DOTALL)

for oldMatch in oldMatches:
    print(oldMatch)

###Now its time to update the files!!!

# Saves the newly updated red book songs in "Երգարան Word Files"
song_list = []
for song_text in matches:
    song_num = re.findall("\d+",song_text)
    # first_line = re.findall("\w   ",match) #First Line is being wack so I'm going to skip and start working with try
    print(song_num[0])
    doc = docx.Document("C:/Users/" + user + "/OneDrive/blankdoctemplate.docx")
    # style = doc.styles
    doc.add_paragraph(song_text)
    font = doc.styles['Normal'].font
    font.name = 'Arial'
    font.size = Pt(22)
    doc.save("C:/Users/" + user + "/OneDrive/Երգարան Word Files/songUpdaterOut/" + str(song_num[0]) + ".docx")


# Saves the newly updated old book songs in "Word Files"
for oldSong_text in oldMatches:
    song_num = re.findall("\d+",oldSong_text) # for finding som num
    title = getOldSongTitle(oldSong_text)
    print(song_num[0])
    doc = docx.Document("C:/Users/" + user + "/OneDrive/blankdoctemplate.docx")
    # style = doc.styles
    doc.add_paragraph(oldSong_text)
    font = doc.styles['Normal'].font
    font.name = 'Arial'
    font.size = Pt(22)
    doc.save("C:/Users/" + user + "/OneDrive/Word songs/" + str(song_num[0]) + " " + title + ".docx")