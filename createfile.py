#This file/module serves as a helper for my newGui.py app
import os, docx, time, re
from glob import glob
import json
from docx.shared import Pt

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

def FindNum(song):
    return song['song'][0]['text']

def getDocTextAndIndentation(filename:str, my_doc):
    """Reads a DOCX file and returns a docx file with the text"""
    doc = docx.Document(filename)
    for p in doc.paragraphs:
        first_line_indent = p.paragraph_format.first_line_indent
        left_indent = p.paragraph_format.left_indent
        right_indent = p.paragraph_format.right_indent
        Placeholder = my_doc.add_paragraph(p.text)
        Placeholder.paragraph_format.space_after = 0
        if first_line_indent is not None:
            Placeholder.paragraph_format.first_line_indent = first_line_indent
        if left_indent is not None:
            Placeholder.paragraph_format.left_indent = left_indent
        if right_indent is not None:
            Placeholder.paragraph_format.right_indent = right_indent
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(22)
        
    return my_doc

#parses the data inputed and sends back a python-docx file object
def getPcSongs(songs, imp, user):
    """parses the data inputed and sends back a python-docx file object

    Args:
        songs (list): A list containing all of the song numbers requested
        imp (list): used to denote either 'n'ew or 'o'ld databases
        user (str): a str denoting what pc this is being run on

    Raises:
        Wrong file name: thrown by a checker that checks to see if the filename matchs with what is found

    Returns:
        docx: a word file containing the requested songs
    """
    user = os.getenv("USERNAME")
    my_doc = docx.Document("C:/Users/" + user + "/OneDrive/Choir Songs Template.docx")
    for x in songs:
        x = str(x)
        y = songs.index(x)
        if 'n' in imp[y]:
            
            try:
                with open("ergaran.json", 'r', encoding='utf-8') as f:
                    ergaran = json.load(f)
                filename = ergaran["SongNum"][x]["latestVersion"]
                # Run a check to make sure that it finds 3 and not 33
                # verification method to double check and make sure that the program has found found the right song
                if (re.findall("Երգարան Word Files"+"\S[0-9]*",filename)[0]) == "Երգարան Word Files\\" + x:
                    my_doc.add_paragraph("[start:song]")
                    getDocTextAndIndentation(filename=filename, my_doc=my_doc)
                    my_doc.add_paragraph("[end:song]")
                else:
                    raise Exception("Wrong file name")
                
            except:
                my_doc.add_paragraph("[start:song]")
                getDocTextAndIndentation(filename="C:/Users/" + user + "/OneDrive/RED Words/" + x + ".docx", my_doc=my_doc)
                my_doc.add_paragraph("[end:song]")
                
        else:
            
            try:
                with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
                    index = json.load(f)
                filename = index["SongNum"][x]["latestVersion"]
                
                # verification method to double check and make sure that the program has found found the right song
                if (re.findall("Word songs"+"\S[0-9]*",filename)[0]) == "Word songs\\" + x:
                    my_doc.add_paragraph("[start:song:old]")
                    getDocTextAndIndentation(filename=filename, my_doc=my_doc)
                    my_doc.add_paragraph("[end:song:old]")
                else:
                    raise Exception("Wrong file name")
            except:
                my_doc.add_paragraph("Error: FileNotFoundError \nSong: " + x + " Old, Could not be located ")
    
    return my_doc

def getPosibleSongs(songs, imp, user):
    posSongList = []
    for x in songs:
        x = str(x)
        y = songs.index(x) # gets loc of x in songs:list
        if 'n' in imp[y]:
            
            try:
                with open("ergaran.json", 'r', encoding='utf-8') as f:
                    ergaran = json.load(f)
                filename = ergaran["SongNum"][x]["latestVersion"]
                # verification method to double-check and make sure that the program has found the right song
                posSong = re.findall("Երգարան Word Files"+"\S[0-9]*",filename)[0]
                if (posSong) == "Երգարան Word Files/" + x: 
                    posSongList.append(re.findall("Երգարան Word Files"+"\S[0-9]*",filename)[0])
            except:
                posSongList.append("RED Words/" + str(x))
        else:
            
            try:
                with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
                    index = json.load(f)
                filename = index["SongNum"][x]["latestVersion"]
                if (re.findall("Word songs"+"\S[0-9]*",filename)[0]) == "Word songs\\" + x:
                    posSongList.append(re.findall("Word songs"+"\S[0-9]*",filename)[0])
            except:
                posSongList.append(str(x) + " Old, Could not be located ")

    return posSongList

