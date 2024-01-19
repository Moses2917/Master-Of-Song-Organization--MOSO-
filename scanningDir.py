import os, datetime, docx, re
def getRecentSongs():
    #Todo: posibily change function to always append to it the latest files instead of just rewriting it always
    # Also bc the program sorts the songs here the current sorting process is now made partly obsolete, but maybe not bc program still needs to sort with3 month window
    import WordSongUpdater
    #     Finds all possible dir/paths to docx files that possibly can be used, with datetime and os
    songBuffer = ""
    user = os.environ.get("USERNAME")
    three_months_from_now = (datetime.date.today() + datetime.timedelta(days=-90)).strftime(
        '%Y')  # currently returns '2023' to use multi funnel/net system to go from big -> fine net
    RelevantDate = (datetime.datetime.today() + datetime.timedelta(days=-90))
    with os.scandir(r'C:\Users\{}\OneDrive\Երգեր'.format(user)) as PosFiles:
        for file in PosFiles:
            if three_months_from_now in file.name:

                if "." in file.name:

                    date = datetime.datetime.strptime(file.name, '%m.%Y')
                    if date > RelevantDate:

                        songBuffer += "\n"+file.path
                        # print(file.path)
                        for docs in os.scandir(r'C:\Users\{}\OneDrive\Երգեր\{}'.format(user,file.name)):

                            #this can be a bit redundant sometimes however its also safer
                            docName = re.sub(".docx", "", docs.name)
                            try:
                                dateD = datetime.datetime.strptime(docName, "%m.%d.%y")
                            except:
                                dateD = datetime.datetime(1970, 1, 1, 0, 0, 0)
                            if dateD > RelevantDate:
                                # pass
                                # print(docName) # this is a str not a os.direntry
                                # print(docs.path) # EX: C:\Users\Armne\OneDrive\Երգեր\09.2023\09.28.23.docx
                                songBuffer += "\nFilename/Date: " + docName
                                songBuffer += "\nSongs in that file: " + WordSongUpdater.getNums(docs.path)
                                # Now it can be passed to WordSongUpdater.getNums()
                else:
                    for folders in os.scandir(r'C:\Users\{}\OneDrive\Երգեր\{}'.format(user,file.name)):
                        # print(folders.path)
                        date = datetime.datetime.strptime(folders.name, '%m.%Y')
                        if date > RelevantDate:
                            songBuffer += "\n"+folders.path
                            docName = re.sub(".docx", "", folders.name)

                            try:
                                dateD = datetime.datetime.strptime(docName, "%m.%Y")

                            except:
                                dateD = datetime.datetime(1970, 1, 1, 0, 0, 0)

                            if dateD > RelevantDate:
                                # pass
                                # print(docName) # this is all of the indiv songs that are rel, now need to check folders
                                for files in os.scandir(r'C:\Users\{}\OneDrive\Երգեր\{}\{}'.format(user,file.name,docName)):
                                    doc2Name = re.sub(".docx", "", files.name)
                                    doc2Name = re.sub("PORC_PORC", "", doc2Name)
                                    doc2Name = re.sub("TESTSAVE", "", doc2Name)

                                    dateD = datetime.datetime.strptime(doc2Name, "%m.%d.%y")

                                    if dateD > RelevantDate:
                                        # print(files.path)
                                        songBuffer += "\nFilename/Date: " + files.name
                                        songBuffer += "\nSongs in that file: " + WordSongUpdater.getNums(files.path)
                                # print(r'C:\Users\{}\OneDrive\Երգեր\{}\{}'.format(user,file.name,folders.name)) # EX: C:\Users\Armne\OneDrive\Երգեր\09.2023\09.28.23.docx
                                # Now it can be passed to WordSongUpdater.getNums()
    with open("RecentSongs.txt",'w',encoding='utf-8') as f:
        f.write(songBuffer)

def getAllNums():
    from WordSongUpdater import getNums
    f=open("AllSongs.txt", 'w', encoding='utf-8')
    bufferList = []
    startDate = datetime.datetime(year=2023,month=1,day=17,)
    with os.scandir(r'C:\Users\{}\OneDrive\Երգեր'.format(os.environ.get("USERNAME"))) as folders:
        for entry in folders:
            if re.match(r'\d',entry.name):  # if file/folder contains a number
                # print(entry.path)
                if "." in entry.name and datetime.datetime.strptime(entry.name, '%m.%Y') >= startDate: #this means it is something like mm.YY
                    # print(entry.name)
                    # print("\nFilename/Date: {}".format(entry.name))
                    bufferList.append("\nFolder Path: {}".format(entry.path))
                    # f.write("\nFilename/Date: {}".format(entry.name))
                    for condesedFolders in os.scandir(entry.path): #gets all the docx files
                       # print("\nSongs in that file: "+ getNums(condesedFolders.path))
                       bufferList.append("\nFilename/Date: {}".format(condesedFolders.name))
                       bufferList.append("\nSongs in that file: "+ getNums(condesedFolders.path))
                        # f.write("\nSongs in that file: "+ getNums(condesedFolders.path))
                else:
                    if not "." in entry.name and (datetime.datetime.strptime(entry.name, '%Y') >= datetime.datetime.strptime('2023', '%Y')):
                        for condesedFileFolders in os.scandir(entry.path):
                            # print(condesedFileFolders)
                            if "." in condesedFileFolders.name and (datetime.datetime.strptime(condesedFileFolders.name, '%m.%Y') > startDate):  # this means it is something like mm.YY
                                # print(entry.name)
                                # print("\nFilename/Date: {}".format(entry.name))
                                f.write("\nFolder Path: {}".format(condesedFileFolders.path))
                                for condesedFoldersDocx in os.scandir(condesedFileFolders.path):  # gets all the docx files
                                    # print("\nSongs in that file: "+ getNums(condesedFoldersDocx.path))
                                    # if ".docx" in condesedFoldersDocx.name:
                                    f.write("\nFilename/Date: {}".format(condesedFoldersDocx.name))
                                    f.write("\nSongs in that file: " + getNums(condesedFoldersDocx.path))
    for filePth in bufferList:
        f.write(filePth)
    f.close()

# getAllNums()

# gets songs fron recentsongs and sorts by last three months
def songCollector(): 
    """Generates a list of all the sunday songs sang in the last three months

    Returns:
        blocked_list: a list containing two sub lists one of songs one for the matching book and another for the filename/date
    """    
    blocked_list =[]
    current_date = datetime.date.today() # should really be

    # Format the date and time
    formatted_date = current_date.strftime('%m.%d.%y')
    # print("The current date is:", formatted_date)
    three_months_from_now = (current_date + datetime.timedelta(days=-90)).strftime('%m.%d.%y')
    # print("Three months ago it was:", three_months_from_now)
    TotalLineCt = len(open('AllSongs.txt','r',encoding='utf-8').readlines())
    CurrentLine = 0
    with open('AllSongs.txt', 'r', encoding='utf-8') as line:
        
        while(CurrentLine<TotalLineCt):
                
            txt = line.readline()
            if "Filename/Date: " in txt:
                date = re.sub("Filename/Date: ", "", txt)
                date = re.findall(r"(.*\d)",date)[0]
                fileDate = date # saving this for later to be used in list
                # Define the date format
                date_format = "%m.%d.%y"
                # Parse the dates into datetime objects
                date1 = datetime.datetime.strptime(three_months_from_now, date_format)
                date2 = datetime.datetime.strptime(date, date_format)
                if date1 < date2:
                    # print("bad dates", date2)#add to blacklist of songs once you have the songs sang
                    if date2.strftime('%A') == "Sunday": # if date is 3 month fresh and also sunday
                        txtNext = line.readline()
                        CurrentLine += 1
                        if "Songs" in txtNext:
                            txtNext = re.sub("Songs in that file: ", "", txtNext)
                            # txtNext = re.sub('', '0', txtNext)
                            txtNext = re.sub(r"''",'INVALID',txtNext)
                            # print(txtNext) #TODO: fix problem of empty strings
                            # print(date2.strftime('%A'))
                            songs = re.findall(r'(\d+)', txtNext)
                            books = re.findall(r'([A-Za-z]+)', txtNext)###
                            # print(songs, books)
                            # lis = [songs,books]
                            blocked_list.append([songs,books,fileDate])
                            # print(lis)
                else:
                    pass
            
            CurrentLine += 1
    return blocked_list

def songChecker(songNum:str, book:str):
    """Finds songNum, then go to that index in books and see if it matchs with the given book var and also check and see if there is an "invaild" string to skip the next book

    Args:
        songNum str: song number being checked
        book str: from olds or new book

    Returns:
        Bool: True if used False if not
    """    
    blackList = songCollector()
    for song in blackList:
        # print(song)
        if songNum in song[0]: #all instances of/with songNum in them
            # print(song)
            bookindex = song[0].index(songNum)
            # print(bookindex)
            print("Book:", song[1][bookindex])
            if song[1][bookindex-1] == 'INVALID':
                bookindex += 1 #Skips the Invaild one, possible weak link which might cause future problems
            booked = song[1][bookindex]
            if book == booked:
                print("Found a match in past 3 months")
                return True
            elif book != booked:
                print("Found nothing")
 
def getSongDate(songNum:str, book:str):
    """Gets the absolute latest date as to when that duplicate song was sang

    Args:
        songNum (str): Unique song identifier.
        book (str): Describes what database its from.

    Returns:
        str: returns a date in str of when that song was last sang
    """    
    blackList = songCollector()
    latestDate = "03.13.20"
    date_format = "%m.%d.%y"
    for song in blackList:
    # print(song)
        if songNum in song[0]: #all instances of/with songNum in them
            # print(song)
            bookindex = song[0].index(songNum)
            # print(bookindex)
            print("Book:", song[1][bookindex])
            if song[1][bookindex-1] == 'INVALID':
                bookindex += 1 #Skips the Invaild one, possible weak link which might cause future problems
            booked = song[1][bookindex]
            if book == booked:
                print(song[2])
                date1 = datetime.datetime.strptime(latestDate, date_format)
                date2 = datetime.datetime.strptime(song[2], date_format)
                if date1 < date2:
                    latestDate = date2.strftime(date_format)
                # else:

            elif book != booked:
                print("Found nothing")
    print("Found a match in past 3 months",latestDate)
    return latestDate

#Translation layer from txt to json
#TODO: Just save in JSON
def jsonifySongList():
    with open("AllSongs.txt",'r',encoding='utf-8') as lines:
        data = lines.read()
        data = data.strip().split("\n")
        result = []
        # basePath = ""
        for line in data:
            songs = []
            if 'Folder Path: ' in line:
                line = re.sub('Folder Path: ', '', line)
                basePath = line
            if 'Filename/Date: ' in line:
                line = re.sub('Filename/Date: ', '', line)
                filenameDate = line
            if 'Songs in that file' in line:
                songs_str = line.split(': ')[1]
                # songs_list = ast.literal_eval(songs_str)
                songs_list = eval(songs_str)
                
                for song in songs_list:
                    song_elements = list(song)
                    
                    # Check if the list is not empty before accessing the first element
                    song_id_list = [element for element in song_elements if element is not None and element.isdigit()]
                    song_type_list = [element for element in song_elements if element is not None and not element.isdigit()]

                    if song_id_list:
                        song_id = song_id_list[0]
                    else:
                        song_id = None

                    if song_type_list:
                        song_type = song_type_list[0]
                    else:
                        song_type = None

                    songs.append({"type": song_type, "id": song_id})
                result.append({
                "songs": songs,
                "basePath": basePath,
                "Filename/Date": filenameDate
                })
                

        # print(result)

        # Print the result as a JSON
        import json
        # print(json.dumps(result, indent=4,ensure_ascii=False))
    return json.dumps(result, indent=4)
    # return result

def search_song(data, song_num, book):
    found_list = []
    found = False
    for item in data:
        for song in item['songs']:
            if song['id'] == song_num and song['type'] == book:
                found_list.append(item)
                found = True
                # return item
    if found:
        return found_list
    return None

def songSearch(song_num,book):
    import json
    data = json.loads(jsonifySongList())

    # Define the search function


    result = search_song(data, song_num, book)
    
    if result:
        # print(f"Found song number {song_num} in book {book} in the file for {result['filename_date']}.")
        for x in result:
            print(x)
    else:
        print(f"Song number {song_num} in book {book} not found.")

# songSearch("320","Old")

# with open("jsonedUp.json", 'w') as f:
#     import json
#     data = json.loads(jsonifySongList())
#     json.dump(data,f,indent="4")