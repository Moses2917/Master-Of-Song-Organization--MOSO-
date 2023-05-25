import re, json

with open("REDergaran.json", 'r', encoding='utf-8') as f:
    index = json.load(f)

for songNum in index["SongNum"]:
    #now we find the title of that song num
    # for Title in index["SongNum"][songNum]["Title"]:
    Title = index["SongNum"][songNum]["Title"]
    try:
        print("Changing: ", index["SongNum"][songNum]["Title"], "To:",re.findall(r"([ա-ֆԱ-Ֆ*].+)",Title)[0])
        index["SongNum"][songNum]["Title"] = re.findall(r"([ա-ֆԱ-Ֆ*].+)",Title)[0]
    except:
        print("no changes were needed for the title")

with open("REDergaran.json", 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=4)