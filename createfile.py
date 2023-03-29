#This file/module serves as a helper for my newGui.py app
import os, docx, time, re
from glob import glob
import json
import xml.etree.ElementTree as ET
from docx.shared import Pt

#for getting the user's desired date and/or location
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

def getTemplate():
    wordFile = open("Choir Songs Template.dotx", 'r', encoding='utf_8')
    template = wordFile.read()
    wordFile.close
    return template

month = time.strftime('%m')
year = time.strftime('%y')
fullYear = time.strftime('%Y')
day = time.strftime('%d')


def process(filename):
    text = ""
    doc = docx.Document(filename)
    for p in doc.paragraphs:
        text += p.text + "\n"
    return text



def date():
    return str(fullYear)


#parses the data inputed and sends back a python-docx file object
def getPcSongs(songs, imp, user):
    my_doc = docx.Document("C:/Users/" + user + "/OneDrive/Choir Songs Template.docx")
    for x in songs:
        x = str(x)
        y = songs.index(x)
        if 'n' in imp[y]:
            
            try:
                filename = glob("C:/Users/" + user + "/OneDrive/Երգարան Word Files/" + x + "*.docx")[0] #gets name
                ##Run a check to make sure that it finds 3 and not 33
                tempFile = ""
                # verification method to double check and make sure that the program has found found the right song
                if (re.findall("Երգարան Word Files"+"\S[0-9]*",filename)[0]) == "Երգարան Word Files\\" + x:
                    tempFile = "[start:song]\n" + process(filename) + "[end:song]"
                else:
                    raise Exception("Wrong file name")
                # tempFile = "[start:song]\n" + process(filename) + "[end:song]"

            except:
                tempFile = "[start:song]\n" + process("C:/Users/" + user + "/OneDrive/RED Words/" + x + ".docx") + "[end:song]"
        else:
            
            try:
                filename = glob("C:/Users/" + user + "/OneDrive/Word songs/" + x + "*")[0] # gets name
                tempFile = ""
                # verification method to double check and make sure that the program has found found the right song
                if (re.findall("Word songs"+"\S[0-9]*",filename)[0]) == "Word songs\\" + x:
                    tempFile = "[start:song:old]\n" + process(filename) + "[end:song:old]"
                else:
                    raise Exception("Wrong file name")
            except:
                tempFile = "Error: FileNotFoundError \nSong: " + x + " Old, Could not be located "
            
        # word.write("\n" + tempFile + '\n')
        my_doc.add_paragraph(tempFile + '\n')#.add_run()

    
    return my_doc

def getPosibleSongs(songs, imp, user):
    posSongList = []
    for x in songs:
        x = str(x)
        y = songs.index(x)
        if 'n' in imp[y]:
            
            try:
                f = open("ergaran.json", 'r', encoding='utf-8')
                ergaran = json.load(f)
                f.close
                # filename = glob("C:/Users/" + user + "/OneDrive/Երգարան Word Files/" + x + "*.docx")[0] #gets name # is now kind of obsolete bc of ergaran.json
                filename = ""
                for songNum in ergaran["SongNum"]:
                    if songNum == x:
                            filename = ergaran["SongNum"][x]["latestVersion"]
                            # print(filename)
                # verification method to double check and make sure that the program has found found the right song
                posSong = re.findall("Երգարան Word Files"+"\S[0-9]*",filename)[0]
                if (posSong) == "Երգարան Word Files/" + x: 
                    posSongList.append(re.findall("Երգարան Word Files"+"\S[0-9]*",filename)[0])
            except:
                posSongList.append("RED Words/" + str(x))
        else:
            
            try:
                filename = glob("C:/Users/" + user + "/OneDrive/Word songs/" + x + "*")[0] # gets name
                # verification method to double check and make sure that the program has found found the right song
                if (re.findall("Word songs"+"\S[0-9]*",filename)[0]) == "Word songs\\" + x:
                    posSongList.append(re.findall("Word songs"+"\S[0-9]*",filename)[0])
            except:
                posSongList.append(str(x) + " Old, Could not be located ")
            
        # word.write("\n" + tempFile + '\n')
        

    
    return posSongList

