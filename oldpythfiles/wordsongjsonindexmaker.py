import json, os, docx, re
folderPth = "C:/Users/{}/OneDrive/Word songs/pptSong/".format(os.environ.get("USERNAME"))
from glob import glob
fileList = glob(folderPth+"*.docx")
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    ct = 0
    # This is made to restrict the script to only the frist couple of lines for efficiency,
    # this does not need all the lines in the song just the first few
    for para in doc.paragraphs:
        if ct <= 1:
            ct+=1
            fullText.append(para.text)
        else:
            # return '\n'.join(fullText)
            fullText='\n'.join(fullText)
            break
    return [fullText, filename]


doc_list = list(map(getText,fileList))

# with open("PPTWordSongs.json", "w", encoding='utf-8') as f:
#     index = json.loads(f.read())

index = json.loads('{"SongNum": {}}')

# index = {
#     "SongNum": {
        
#     }
# }
for p in doc_list:
    # print(p)
    text = p[0]
    filename = p[1]
    songNum = re.findall("[\d]+",text)
    filename = re.sub(r"C:\\Users\\\w+\\OneDrive\\","",filename)
    posTitle = re.sub(r"Word songs\\pptSong\\\d+\s","",filename)
    index["SongNum"][songNum[0]] = {
        "Title": posTitle,
        "latestversion": filename,
        "v1": filename,
    }
    # print(index)

with open("PPTWordSongs.json", "w", encoding='utf-8') as f:
    index = json.dump(index,f,ensure_ascii=False,indent=4)

#bc it takes to long I will only load song 1 and work from there
# print(doc_list[0])

# text = getText(r"C:\Users\Armne\OneDrive\Word songs\pptSong\522 Այս է այն գետը որ բխում է գահից.docx")
# print(re.sub(r"[\d+\s]","",text[0]))

# re.sub("C:\\Users\\\w+\\OneDrive\\","",text)
# index = {
#     "SongNum": {
        
#     }
# }
# songNum = re.findall("[\d]+",text[0])[0]
# print(type(songNum)) #it is a string


# index["SongNum"] = {
#     songNum:{
#         "Title": posTitle,
#         "latestversion": filename,
#         "v1": filename,
#     }
# }