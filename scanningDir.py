import os, time, datetime,docx, re
def getAllNums():
    import WordSongUpdater
    f=open("RecentSongs.txt", 'w', encoding='utf-8')
    with os.scandir(r'C:\Users\{}\OneDrive\Երգեր'.format(os.environ.get("USERNAME"))) as files:
        for entry in files:
            # print(entry)
            if ".20" in entry.name:
                with os.scandir(r'C:\Users\{}\OneDrive\Երգեր/'.format(os.environ.get("USERNAME"))+os.fsdecode(entry.name)) as files:
                    fPath = r'C:\Users\{}\OneDrive\Երգեր/'.format(os.environ.get("USERNAME"))+os.fsdecode(entry.name)
                    print(fPath)
                    f.write("\n"+fPath)
                    for entry in files:
                        # print(entry)
                        if ".docx" and ".23" in entry.name:
                            # print(os.path.join(os.getcwd(), entry.name))#have full file path, just need to check for if its
                            print("\nFilename/Date:",entry.name, "\nSongs in that file: ")
                            print(WordSongUpdater.getNums(os.path.join(fPath, entry.name)))
                            f.write("\nFilename/Date: " + entry.name + "\nSongs in that file: ")
                            f.write(WordSongUpdater.getNums(os.path.join(fPath, entry.name)))
    f.close()
# getAllNums()
#Add pop-up window to check if indiv. song has been sang, also supply date/file name with it

# Using a regex algo to sort through RecentSongs.txt, extract two things, 1. Date and 2. the list of songs sang on that date


# def songChecker(book, songNum):
def songCollector(): 
    blocked_list =[]
    current_date = datetime.date.today()

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
                # Define the date format
                date_format = "%m.%d.%y"
                # Parse the dates into datetime objects
                date1 = datetime.datetime.strptime(three_months_from_now, date_format)
                date2 = datetime.datetime.strptime(date, date_format)
                if date1 < date2:
                    # print("bad dates", date2)#add to blacklist of songs once you have the songs sang
                    if date2.strftime('%A') == "Sunday":
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
                            lis = [songs,books]
                            blocked_list.append([songs,books])
                            # print(lis)
                else:
                    pass
            
            CurrentLine += 1
    return blocked_list
       
    def done():
        recentSongs = open("RecentSongs.txt", 'r', encoding='utf-8')
        lines = recentSongs.readlines()
        # print(lines)
        for line in lines:
            recentSongs.readline()
            if "Filename/Date:" in line:
                line = re.sub("Filename/Date: ", "", line[0])
                print(line)
                songDate = re.findall(r"(.*\d)",line)[0]
                # print(songDate) #relieably sorts out just the date, now need to test the dateChecker
                # if songDate is smaller than three_Months ago date, then harvest the songs with n/o and add to no sing list

                # Define the date format
                date_format = "%m.%d.%y"
                # Parse the dates into datetime objects
                date1 = datetime.datetime.strptime(three_months_from_now, date_format)
                date2 = datetime.datetime.strptime(songDate, date_format)
                if date1 < date2:
                    print(songDate)
                    nxtLine=lines[lines[line + 1]]
                    if "song" in nxtLine:
                        print(nxtLine)

                else:
                    lines = ""

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

        
        
        

# songCollector()
# songChecker(songNum='623', book='Old')