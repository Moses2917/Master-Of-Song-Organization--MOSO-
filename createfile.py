#This file/module serves as a helper for my newGui.pyw app, otherwise known as MOSO
import os, docx, time, re
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
    # print(song)
    return song['song'][0]['text']

def getDocTextAndIndentation(filename:str, my_doc):
    """Reads a DOCX file and returns a docx file with the text"""
    user = os.environ.get("USERNAME")
    doc = docx.Document("C:/Users/" + user + "/OneDrive/" + filename)
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
    user = os.environ.get("USERNAME")
    my_doc = docx.Document("C:/Users/" + user + "/OneDrive/Choir Songs Template.docx")
    for x in songs:
        x = str(x)
        y = songs.index(x)
        if 'n' in imp[y]:
            
        
            with open("ergaran.json", 'r', encoding='utf-8') as f:
                ergaran = json.load(f)
            filename = ""
            if x in ergaran["SongNum"]:
                filename = ergaran["SongNum"][x]["latestVersion"]
                my_doc.add_paragraph("[start:song]")
                getDocTextAndIndentation(filename=filename, my_doc=my_doc)
                my_doc.add_paragraph("[end:song]")
            else:
                my_doc.add_paragraph("[start:song]")
                getDocTextAndIndentation(filename="RED Words/" + x + ".docx", my_doc=my_doc)
                my_doc.add_paragraph("[end:song]")
                
        else:
            with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
                OldErgaran = json.load(f)
            filename = ""
            if x in OldErgaran["SongNum"]:
                filename = OldErgaran["SongNum"][x]["latestVersion"]
            else:
                my_doc.add_paragraph("Error: FileNotFoundError \nSong: " + x + " Old, Could not be located ")
                
            my_doc.add_paragraph("[start:song:old]")
            getDocTextAndIndentation(filename=filename, my_doc=my_doc)
            my_doc.add_paragraph("[end:song:old]")


    
    my_doc.add_page_break()
    
    return my_doc

def getPosibleSongs(songs, imp):
    posSongList = []
    user = os.environ.get("USERNAME")
    for x in songs:
        x = str(x)
        y = songs.index(x)
        if 'n' in imp[y]:
            
            try:
                with open("ergaran.json", 'r', encoding='utf-8') as f:
                    ergaran = json.load(f)
                # filename = glob("C:/Users/" + user + "/OneDrive/Երգարան Word Files/" + x + "*.docx")[0] #gets name # is now kind of obsolete bc of ergaran.json
                filename = ""
                if x in ergaran["SongNum"]:
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
                with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
                    OldErgaran = json.load(f)
                filename = ""
                if x in OldErgaran["SongNum"]:
                    filename = OldErgaran["SongNum"][x]["latestVersion"]
                
                # verification method to double check and make sure that the program has found found the right song
                if (re.findall("Word songs"+"\S[0-9]*",filename)[0]) == "Word songs\\" + x:
                    posSongList.append(re.findall("Word songs"+"\S[0-9]*",filename)[0])
            except:
                posSongList.append(str(x) + " Old, Could not be located ")
            
        # word.write("\n" + tempFile + '\n')
        

    
    return posSongList

