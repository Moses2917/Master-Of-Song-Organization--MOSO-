import os, datetime, docx, re
def getAllNums():
    import WordSongUpdater
    f=open("RecentSongs.txt", 'w', encoding='utf-8')
    current_date = datetime.datetime.today().strftime('%Y')
    three_months_from_now = (datetime.date.today() + datetime.timedelta(days=-90)).strftime('%Y') #currently returns '2023'
    with os.scandir(r'C:\Users\{}\OneDrive\Երգեր'.format(os.environ.get("USERNAME"))) as files:
        for entry in files:

            if (not "." in entry.name) and (three_months_from_now in entry.name): #this means that entry is a folder relevant to this year ->
                print("Folder:", entry.name) ##Folder: '2023'
                for content in os.scandir(r'C:\Users\{}\OneDrive\Երգեր'.format(os.environ.get("USERNAME"))):
                    RelevantDate = (datetime.datetime.today() + datetime.timedelta(days=-90)) # Window of relevancy Now compare the folder names to see if it is relevant to last three months, then pass to next if statement
                    try:
                        date = datetime.datetime.strptime(content.name,'%m.%Y')
                    except:
                        try:
                            date = datetime.datetime.strptime(content.name, '%Y')
                            RelevantDate = datetime.datetime(RelevantDate, '%Y')
                        except:
                            date = datetime.datetime(1970, 1, 1, 0, 0, 0) #Unix epoch

                    if date > RelevantDate:
                        entry = content
                        print(entry)

            if (".20" in entry.name) or (): # if current date - 3 months yr is same then get folders if no "." in string #Todo: update to compare names like above
                with os.scandir(r'C:\Users\{}\OneDrive\Երգեր/'.format(os.environ.get("USERNAME"))+os.fsdecode(entry.name)) as files:
                    fPath = r'C:\Users\{}\OneDrive\Երգեր/'.format(os.environ.get("USERNAME"))+os.fsdecode(entry.name)
                    # print(fPath)
                    f.write("\n"+fPath)
                    for entry in files:
                        # print(entry)
                        if ".docx" and ".23" in entry.name:#Todo: Future proof for 2024, with datetime
                            # print(os.path.join(os.getcwd(), entry.name))#have full file path, just need to check for if its
                            # print("\nFilename/Date:",entry.name, "\nSongs in that file: ")
                            # print(WordSongUpdater.getNums(os.path.join(fPath, entry.name)))
                            f.write("\nFilename/Date: " + entry.name + "\nSongs in that file: ")
                            f.write(WordSongUpdater.getNums(os.path.join(fPath, entry.name)))
    f.close()
getAllNums()
#Add pop-up window to check if indiv. song has been sang, also supply date/file name with it

# Using a regex algo to sort through RecentSongs.txt, extract two things, 1. Date and 2. the list of songs sang on that date


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
                