import os, datetime, docx, re
def getAllDir():
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
                        songBuffer += "\n"+folders.path
                        date = datetime.datetime.strptime(folders.name, '%m.%Y')
                        if date > RelevantDate:
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
    # startDate = "01.17.23"
    startDate = datetime.datetime(year=2023,month=1,day=17,)
    with os.scandir(r'C:\Users\{}\OneDrive\Երգեր'.format(os.environ.get("USERNAME"))) as folders:
        for entry in folders:
            print(entry.name)
            folderDate = datetime.datetime.strptime(entry.name, '%m.%Y')
            if "." in entry.name and startDate >= folderDate:
                f.write("\n" + entry.path)
                with os.scandir(entry.path) as folderFiles:
                    for file in folderFiles:
                        fileDate = datetime.datetime.strptime(file.name, '%m.%d.%y')
                        if startDate >= fileDate and ".docx" in file.name:
                            f.write("\nFilename/Date: " + file.name + "\nSongs in that file: ")
                            f.write(getNums(file.path))

    f.close()
getAllNums()
# getAllDir()
# def songChecker(book, songNum):
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
    print("Three months ago it was:", three_months_from_now)
    TotalLineCt = len(open('RecentSongs.txt','r',encoding='utf-8').readlines())
    CurrentLine = 0
    with open('RecentSongs.txt', 'r', encoding='utf-8') as line:
        
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
        book (str): from olds or new book

    Returns:
        Bool: True if used False if ok to use
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
        songNum (str): _description_
        book (str): _description_

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
                