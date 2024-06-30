import json
import os, datetime, docx, re


def getRecentSongs():
    # Todo: posibily change function to always append to it the latest files instead of just rewriting it always
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

                        songBuffer += "\n" + file.path
                        # print(file.path)
                        for docs in os.scandir(r'C:\Users\{}\OneDrive\Երգեր\{}'.format(user, file.name)):

                            # this can be a bit redundant sometimes however its also safer
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
                    for folders in os.scandir(r'C:\Users\{}\OneDrive\Երգեր\{}'.format(user, file.name)):
                        # print(folders.path)
                        date = datetime.datetime.strptime(folders.name, '%m.%Y')
                        if date > RelevantDate:
                            songBuffer += "\n" + folders.path
                            docName = re.sub(".docx", "", folders.name)

                            try:
                                dateD = datetime.datetime.strptime(docName, "%m.%Y")

                            except:
                                dateD = datetime.datetime(1970, 1, 1, 0, 0, 0)

                            if dateD > RelevantDate:
                                # pass
                                # print(docName) # this is all of the indiv songs that are rel, now need to check folders
                                for files in os.scandir(
                                        r'C:\Users\{}\OneDrive\Երգեր\{}\{}'.format(user, file.name, docName)):
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
    with open("RecentSongs.txt", 'w', encoding='utf-8') as f:
        f.write(songBuffer)


def getAllNums():
    """
    Retrieves all songs from the 'Երգեր' directory and its subdirectories that were created or modified after January 17, 2023.
    The songs are stored in a text file named 'AllSongs.txt' in the current working directory.
    
    Parameters:
    None
    
    Returns:
    None
    """
    from WordSongUpdater import getNums
    f = open("AllSongs.txt", 'w', encoding='utf-8')
    bufferList = []
    startDate = datetime.datetime(year=2023, month=1, day=17)
    with os.scandir(r'C:\Users\{}\OneDrive\Երգեր'.format(os.environ.get("USERNAME"))) as folders:
        for entry in folders:
            if re.match(r'\d', entry.name):  # if file/folder contains a number
                # print(entry.path)
                if "." in entry.name and datetime.datetime.strptime(entry.name,
                                                                    '%m.%Y') >= startDate:  # this means it is something like mm.YY
                    # print(entry.name)
                    # print("\nFilename/Date: {}".format(entry.name))
                    bufferList.append("\nFolder Path: {}".format(
                        "Երգեր/" + entry.name))  # in theory could just make it only folder name
                    # f.write("\nFilename/Date: {}".format(entry.name))
                    for condesedFolders in os.scandir(entry.path):  # gets all the docx files
                        # print("\nSongs in that file: "+ getNums(condesedFolders.path))
                        bufferList.append("\nFilename/Date: {}".format(condesedFolders.name))
                        bufferList.append("\nSongs in that file: " + getNums(condesedFolders.path))
                        # f.write("\nSongs in that file: "+ getNums(condesedFolders.path))
                else:
                    if not "." in entry.name and (
                            datetime.datetime.strptime(entry.name, '%Y') >= datetime.datetime.strptime('2023', '%Y')):
                        for condesedFileFolders in os.scandir(entry.path):
                            # print(condesedFileFolders)
                            if "." in condesedFileFolders.name and (datetime.datetime.strptime(condesedFileFolders.name,
                                                                                               '%m.%Y') > startDate):  # this means it is something like mm.YY
                                # print(entry.name)
                                # print("\nFilename/Date: {}".format(entry.name))
                                f.write(
                                    "\nFolder Path: {}".format("Երգեր/" + entry.name + "/" + condesedFileFolders.name))
                                for condesedFoldersDocx in os.scandir(
                                        condesedFileFolders.path):  # gets all the docx files
                                    # print("\nSongs in that file: "+ getNums(condesedFoldersDocx.path))
                                    # if ".docx" in condesedFoldersDocx.name:
                                    f.write("\nFilename/Date: {}".format(condesedFoldersDocx.name))
                                    f.write("\nSongs in that file: " + getNums(condesedFoldersDocx.path))
    for filePth in bufferList:
        f.write(filePth)
    f.close()


# getAllNums() #If left uncommented can cause errors during use of MOSO

# gets songs fron recentsongs and sorts by last three months
def songCollector():
    """Generates a list of all the sunday songs sang in the last three months

    Returns:
        blocked_list: a list containing two sub lists one of songs one for the matching book and another for the filename/date
    """
    from json import load
    blocked_list = []
    current_date = datetime.date.today()  # should really be

    # Format the date and time
    formatted_date = current_date.strftime('%m.%d.%y')
    # print("The current date is:", formatted_date)
    three_months_from_now = (current_date + datetime.timedelta(days=-90)).strftime('%m.%d.%y')
    # print("Three months ago it was:", three_months_from_now)

    with open('songs.json', 'r', encoding='utf-8') as f:
        allSongs = load(f)

    # for key in allSongs:
    #     date = key
    #     date = re.findall(r"(.*\d)", date)[0]

    blocked_dict = {}
    for key in allSongs:
        date = key
        date = re.findall(r"(.*\d)", date)[0]
        fileDate = date  # saving this for later to be used in list
        # Define the date format
        date_format = "%m.%d.%y"
        # Parse the dates into datetime objects
        date1 = datetime.datetime.strptime(three_months_from_now, date_format)
        date2 = datetime.datetime.strptime(date, date_format)
        if date1 < date2:
            # print("bad dates", date2)#add to blacklist of songs once you have the songs sang
            if date2.strftime('%A') == "Sunday":  # if date is 3 month fresh and also sunday
                blocked_list.append([
                    eval(allSongs[key]['songList']),  # [('book','songnum'), ('book','songnum'), ('book','songnum')]
                    fileDate
                ])
                blocked_dict[fileDate] = {
                    'songList': allSongs[key]['songList'],
                    'basePth': allSongs[key]['basePth'],

                }
                # print(lis)
    return blocked_dict
    # return blocked_list

def search_song(data: json, song_num, book):
    """
    Searches for a song in the given data based on the song number and book.

    Parameters:
        data (json): The data to search for the song.
        song_num (str): The number of the song to search for.
        book (str): The book to search for the song in.

    Returns:
        list or None: A list of dictionaries containing the filename/date, basePath, and songList if the song is found, or None if the song is not found.
    """
    found_list = []
    found = False
    for item in data:
        songList = eval(data[item]['songList'])
        for song in songList:
            if song[1] == song_num and song[0] == book:
                found_list.append({
                    'Filename/Date': item,
                    'basePath': data[item]['basePth'],
                    'songs': songList

                })
                found = True
                # return item
    if found:
        return found_list
    return None


def songSearch(song_num:str, book:str):
    """
    A function that searches for a song based on the song number and book provided.

    Parameters:
        song_num (str): The number of the song to search for.
        book (str): The book to search for the song in.

    Returns:
        dict: A dictionary containing information about the found song if it exists, None otherwise.
    """
    import json
    with open('songs_cleaned.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if (book == "REDergaran") or (book == "New"):
        book = 'New'
    if (book == "Old") or (book == "wordSongsIndex"):
        book = 'Old'

    # Define the search function
    result = search_song(data, song_num, book)

    if result:
        # print(f"Found song number {song_num} in book {book} in the file for {result['filename_date']}.")

        # for x in result:
        #     print(x)

        return result
    else:
        print(f"Song number {song_num} in book {book} not found.")
        return None

# print(songSearch("817","Old"))

def songChecker(book: str, songNum: str):
    """Finds songNum, then go to that index in books and see if it matches with the given book var and also check and see if there is an "invalid" string to skip the next book

    Args:
        songNum str: song number being checked
        book str: from olds or new book

    Returns:
        Bool: True if used False if not
        Str: Returns the date it was sang if true
    """

    blocked_list = songCollector()
    date_format = "%m.%d.%y"
    # print(blocked_list)
    song_search_results = search_song(blocked_list, songNum, book)
    date_newest = datetime.datetime.strptime("01.01.70", date_format)
    if song_search_results:
        # print(song_search_results)
        for key in song_search_results:
            print(key['Filename/Date'])
            date_compare = datetime.datetime.strptime(key['Filename/Date'], date_format)
            if date_newest < date_compare:
                date_newest = date_compare
        return True, date_newest.strftime(date_format)
        return True, date_newest
    return False

def toJson():
    """Generates a json version of AllSongs.txt and save it to the disk
    underneath the same name, so AllSongs.json
    """
    import json
    with open("AllSongs.txt", 'r', encoding='utf-8') as lines:
        data = lines.read()
        data = data.strip().split("\n")
        result = {}
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
                    song_type_list = [element for element in song_elements if
                                      element is not None and not element.isdigit()]

                    if song_id_list:
                        song_id = song_id_list[0]
                    else:
                        song_id = None

                    if song_type_list:
                        song_type = song_type_list[0]
                    else:
                        song_type = None

                    songs.append({"type": song_type, "id": song_id})

                result.update({
                    filenameDate: {
                        "songs": songs,
                        "basePath": basePath,
                    }})
    with open('allSongs.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


# TODO Handle case where a file is deleted and no longer exists think file deletions and file renaming
# could do a sort of git difference, where if it doesn't find the file, but it exists in the index, it will be deleted
def findNewFiles():  # is for finding new files so as to only go through and add those insted of the whole library, which in the near future will be a headache when it gets bigger
    """This will make a dict. stored and accessed as a json file. It will store the name of the doc, as well as all
    songs it found in the doc, a basepath where the os path for onedrive can be appended, and it will store the last
    modified date, so when searching for files to update it can ignore certain ones whose modified date has not changed.

    Returns:
        None: Saves a json file.
    """

    def check_blacklist(text):
        blacklist = ['Սուրբ ծնունդ', 'Պենտեկոստե', 'Զատիկ', 'Գոհաբանության Օր', 'Wedding', '2020', '2021',
                     '2022']  # list of unneeded dirs
        return any(item in text for item in blacklist)

    def fileCrawler(filePth: str):  # is_file or is_folder

        os.scandir(filePth)

    # toJson() #run this to update the json index -_-
    OneDrivePth = os.environ.get("OneDrive")  # gets the base path to onedrive from enviornment variables!

    ErgerFolder = os.scandir(OneDrivePth + "\\Երգեր")
    blacklist = ['Սուրբ ծնունդ', 'Պենտեկոստե', 'Զատիկ', 'Գոհաբանության Օր', 'Wedding', '2020', '2021',
                 '2022', '01.2023']  # list of unneeded dirs
    blacklist.extend(['02.2023', '03.2023', '04.2023', '05.2023']) # additional dates where the algo was buggy and reported the wrong song nums
    with os.scandir(OneDrivePth + "\\Երգեր") as ErgerFolders:
        filePths = []
        for ergfolder in ErgerFolders:
            if ergfolder.name not in blacklist:
                # Circa 4/23/2024
                # returns:
                # C:\Users\Armne\OneDrive\Երգեր\01.2024
                # C:\Users\Armne\OneDrive\Երգեր\02.2024
                # C:\Users\Armne\OneDrive\Երգեր\03.2024
                # C:\Users\Armne\OneDrive\Երգեր\04.2024
                # C:\Users\Armne\OneDrive\Երգեր\2023
                if '.' in ergfolder.name:
                    # must be within current yr, so not in a folder like '2023'
                    # these folders go by the format of Month.Yr
                    # Ex:
                    # 01.2024
                    # 02.2024
                    # 03.2024
                    # 04.2024
                    file_path = ergfolder.name
                    file_path.split('.')[1] #gets the extension
                    if 'lnk' not in file_path: # filters out any .lnk extentsion 
                        basePth = 'Երգեր\\' + ergfolder.name
                        print(basePth)
                        filePths.append([
                            ergfolder.path,
                            basePth
                        ])  # add to a stack(array) for processing later via filePths.pop

                else:
                    with os.scandir(ergfolder.path) as fullYrFolder:
                        for months in fullYrFolder:
                            if months.name not in blacklist:  # to filter out 01.2023 which is made with MOSO, also
                                basePth = 'Երգեր\\' + ergfolder.name + "\\" + months.name
                                # replaces a lot of datetime calls
                                filePths.append([
                                    months.path,
                                    basePth
                                ])

    # begin processing the files
    from json import load, dump
    from WordSongUpdater import getNums
    from datetime import datetime
    from os import stat
    with open("songs.json", mode='r', encoding='utf-8') as f:
        allsongs = load(f)
    
    for filepth, basePth in filePths:
        with os.scandir(filepth) as songFolder:
            for songs in songFolder:
                if allsongs.get(songs.name, None):
                    # lookup file in index, and if none do not run code go to else statement
                    dateModOnFile = datetime.fromtimestamp(allsongs[songs.name]['dateMod'])
                    currDateMod = datetime.fromtimestamp(stat(songs.path).st_mtime)

                    # if it exists in the index then do this after setting vars for comparison of dates
                    if not (currDateMod <= dateModOnFile):
                        # if the date modified of a file is greater than the one on file repalce it
                        allsongs[songs.name] = {
                            'dateMod': stat(songs.path).st_mtime,
                            'path': songs.path,
                            'basePth': basePth,
                            'songList': getNums(songs.path)
                        }
                        print("Updated this file", songs.name)
                else:
                    allsongs[songs.name] = {
                        'dateMod': stat(songs.path).st_mtime,
                        'path': songs.path,
                        'basePth': basePth,
                        'songList': getNums(songs.path)
                    }

    # save to json
    with open("songs.json", mode='w', encoding='utf-8') as saveFile:
        dump(allsongs, saveFile, indent=4, ensure_ascii=False)
    
    
    # Same as above but for songs_cleaned.json which has stricter date reqs
    with open("songs_cleaned.json", mode='r', encoding='utf-8') as f:
        allsongs = load(f)
    # allsongs = {} # uncomment this if you want to start from scratch or use this when making a new json, not based on songs.json
    for filepth, basePth in filePths:
        with os.scandir(filepth) as songFolder:
            for songs in songFolder:
                if allsongs.get(songs.name, None):
                    # lookup file in index, and if none do not run code go to else statement
                    dateModOnFile = datetime.fromtimestamp(allsongs[songs.name]['dateMod'])
                    currDateMod = datetime.fromtimestamp(stat(songs.path).st_mtime)

                    # if it exists in the index then do this after setting vars for comparison of dates
                    if not (currDateMod <= dateModOnFile):
                        # if the date modified of a file is greater than the one on file repalce it
                        allsongs[songs.name] = {
                            'dateMod': stat(songs.path).st_mtime,
                            'path': songs.path,
                            'basePth': basePth,
                            'songList': getNums(songs.path)
                        }
                        print("Updated this file", songs.name)
                else:
                    allsongs[songs.name] = {
                        'dateMod': stat(songs.path).st_mtime,
                        'path': songs.path,
                        'basePth': basePth,
                        'songList': getNums(songs.path)
                    }
                    
    with open("songs_cleaned.json", mode='w', encoding='utf-8') as saveFile:
        dump(allsongs, saveFile, indent=4, ensure_ascii=False)


# Uncomment this to manually update the index
print(findNewFiles())