from os import environ as env
import re
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import json
#Setup mongodb
from pymongo import MongoClient
import lyric_search_engine

# with open('{}\\Documents\\Code\\mongoPass.txt'.format(env.get("OneDrive")), 'r') as mongoPass:
#     uri = "mongodb+srv://{}@cluster0.kgkoljn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(mongoPass.read()) #env.get('mongo_user')

# Create a new client and connect to the server
# client = MongoClient(uri)
# songDB = client.get_database("songs")
# songDB = songDB.get_collection("allSongs")

ENV_FILE = find_dotenv("{}\Documents\Code\.env".format(env.get("OneDrive")))
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)

app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

#This route is responsible for actually saving the session for the user, so when they visit again later, they won't have to sign back in all over again.
@app.route("/callback", methods=["GET", "POST"])
def callback():
    """
    Handles the callback from the authorization server.

    This function is responsible for exchanging the authorization code for an access token,
    storing the user's session, and redirecting the user to the temporary home page.

    Parameters:
    None

    Returns:
    redirect: A redirect response to the temporary home page.
    """
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    # print(session["user"])
    #remember to flash('Բարի Գալուստ, {{session.user.userinfo.name}}!')
    # return redirect("/")
    return redirect(url_for('temp_home'))

#the /login route, users will be redirected to Auth0 to begin the authentication flow.
@app.route("/login")
def login():
    """
    This function defines the /login route, which redirects users to Auth0 to begin the authentication flow.
    It does not take any parameters and returns the authorization redirect response from Auth0.
    """
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


#this route handles signing a user out from your application.
@app.route("/logout")
def logout():
    """
    Handles user logout by clearing the session and redirecting to Auth0's logout endpoint.

    Returns:
        redirect: A redirect response to Auth0's logout endpoint.
    """
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("song_info", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

#Function to check the eligability of user to access the webpage, BOOL
def isUserAllowed(email):
    """
    Checks if the provided email is allowed to access the webpage.
    
    Args:
        email (str): The email to be checked.
    
    Returns:
        bool: True if the email is allowed, False otherwise.
    """
    with open("{}\\Documents\\Code\\allowedEmails.csv".format(env.get("OneDrive")), 'r') as f:
        return email in f.read()

# Table data loading logic
def load_table_data(book:str):
    """Reads the respective index file for the book given, and will return a dict

    Args:
        book (str): name of book, can be REDergaran or wordSongIndex

    Returns:
        dict: a dict containing all of the songs in that index
    """
    try:
        with open(f'{book}.json', mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data.get('SongNum')
    except FileNotFoundError:
        return None

def openWord(songNum, book):
    """
    Opens a word document based on the provided song number and book, 
    and returns the contents of the document as a HTML formatted string.

    Args:
        songNum (int): The number of the song to be opened.
        book (str): The name of the book containing the song.

    Returns:
        str: A HTML formatted string containing the contents of the word document.
    """
    from docx import Document
    #Used to find and open word doc, sends back a html formated str of it
    
    if ("word" in book.lower() or "old" in book.lower()):
        with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        with open("REDergaran.json", 'r', encoding='utf-8') as f:
            index = json.load(f)
    
    if index["SongNum"].get(songNum,None):
        songPth = index["SongNum"][songNum]["latestVersion"]
        filePth = env.get("OneDrive")+"\\"+songPth #find pth from index, and attach the location for onedrive
        doc = Document(filePth) #load doc file
        docParagraphs = doc.paragraphs # returns a list of doc paragrpahs from which text will be extracted
        text = ''
        
        for para in docParagraphs:
            text += para.text + '\n'
        
        # Split the text into chunks based on line breaks
        chunks = text.split('\n\n')
        
        # Convert chunks to HTML
        html_chunks = []
        for chunk in chunks:
            lines = chunk.split('\n')
            html_lines = ['<p>' + line + '</p>' for line in lines]
            html_chunk = ''.join(html_lines)
            html_chunks.append(html_chunk)

        # Join the chunks with line breaks, adding or subtracting br will add or subtract the breaks between the paragraphs
        html_text = '<br>'.join(html_chunks)
        return html_text

@app.route('/old', methods=['GET', 'POST'])
def song_info():
    """
    This is deprecated.

    This function is used to display the song information in the form of a webpage. It returns a Flask response object that contains the HTML for the webpage. The webpage displays the song number, title, and author of the song, as well as various other information such as the date the song was published, the number of pages in the song, and the number of verses in the song. The webpage also includes a form that allows the user to enter a new song number and retrieve information about that song. If the user is logged in as an admin, the webpage also includes a form that allows the user to enter a new song number and retrieve information about that song, as well as a form that allows the user to enter a new song number and retrieve information about a specific version of that song. The webpage also includes links to various other pages on the website, such as the song index and the search page.

    Returns:
        Response: A Flask response object that contains the HTML for the webpage.
    """
    song_info = None
    current_values = None
    is_found = False
    if session.get('user', None):
        if isUserAllowed(session['user']['userinfo']['email']):
            
            if request.method == 'POST':
                
                song_num = request.form.get('songNum')
                book = request.form.get('book')
                Bool_Lyrics = request.form.get('lyrics', False)
                
                if Bool_Lyrics:
                    return render_template('song.html', lyrics = openWord(song_num, book), book=book) #sending the book var inorder for the back button to function properly
                
                with open(f'{book}.json',encoding='utf-8') as f:
                    data = json.load(f)
                
                songs = data.get('SongNum')  # Get the songs under the "SongNum" key
                song_info = songs.get(song_num)
                
                if song_info:
                    # Save the current values before they are edited
                    current_values = song_info.copy()
                    if not current_values:
                        flash("That song does not exist",'error')
                # else:
                #     flash("That song does not exist")
                    
                if request.form.get('edit'):
                    song_info['key'] = request.form.get('key')
                    song_info['speed'] = request.form.get('speed')
                    song_info['style'] = request.form.get('style')
                    song_info['song_type'] = request.form.get('Song Type')
                    # song_info['Worship_Song'] = request.form.get('Worship_Song')
                    song_info['timeSig'] = request.form.get('Time Signature')
                    song_info['Comments'] = request.form.get('Comments')
                    songs["SongNum"] = song_info
                    # with open(f'{book}.json', 'w', encoding='utf-8') as f:  # Save the changes to the same file
                    #     json.dump(songs, f, indent=4, ensure_ascii=False)  # Write the whole data back to the file
                
                if request.form.get('submit'):
                    song_info['key'] = request.form.get('key')
                    song_info['speed'] = request.form.get('speed')
                    song_info['style'] = request.form.get('style')
                    song_info['song_type'] = request.form.get('Song Type')
                    # song_info['Worship_Song'] = request.form.get('Worship_Song')
                    song_info['timeSig'] = request.form.get('Time Signature')
                    song_info['Comments'] = request.form.get('Comments')
                    songs[song_num] = song_info
                    # if song_info:
                    #     return flash("That song does not exist",'error')
                with open(f'{book}.json', 'w', encoding='utf-8') as f:  # Save the changes to the same file
                    json.dump(data, f, indent=4, ensure_ascii=False)  # Write the whole data back to the file
                
            return render_template('song_info.html', session=session.get('user'), song_info=song_info, current_values=current_values) #add pretty=json.dumps(session.get('user'), indent=4) for debuging auth
        
        else:
            return redirect('logout')
    
    return render_template('song_info.html', session=session.get('user'))

def saveHtml(filePth, WordDoc):
    """
    Saves the contents of a Word document to an HTML file to later be displayed.

    Parameters:
        filePth (str): The path to the Word document file.
        WordDoc (str): The name of the Word document.

    Returns:
        None
    """
    from docx import Document

    # songPth = r"C:\Users\Armne\OneDrive\Երգեր\Պենտեկոստե\2024\2024 Պենտեկոստե.docx"
    # filePth = songPth  # find pth from index, and attach the location for onedrive
    doc = Document(filePth)  # load doc file
    docParagraphs = doc.paragraphs  # returns a list of doc paragrpahs from which text will be extracted
    text = ''

    for para in docParagraphs:
        text += para.text + '\n'

    # Split the text into chunks based on line breaks
    chunks = text.split('\n\n')

    # Convert chunks to HTML
    html_chunks = []
    for chunk in chunks:
        lines = chunk.split('\n')
        html_lines = ['<p>' + line + '</p>' for line in lines]
        html_chunk = ''.join(html_lines)
        html_chunks.append(html_chunk)

    # Join the chunks with line breaks, adding or subtracting br will add or subtract the breaks between the paragraphs
    html_text = '<br>'.join(html_chunks)
    onedrive = env.get("OneDrive")
    with open(rf"{onedrive}\Documents\Code\Python\htmlsongs\{WordDoc}.txt", 'w', encoding='utf-8') as f:
        f.write(html_text)

# @app.route('/pentecost', methods=['GET'])
# def DayofPentecost():
#     import threading as th
#     songPth = r"C:\Users\Armne\OneDrive\Երգեր\Պենտեկոստե\2024\2024 Պենտեկոստե.docx"
#     MS_WORD = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
#     wordDocThread = th.Thread(target=saveHtml)#, args=[MS_WORD, songPth])
#     wordDocThread.start()
#     # saveHtml()
#     with open(r"C:\Users\Armne\OneDrive\Documents\Code\Python\templates\songLyr.txt", 'r', encoding='utf-8') as f:
#         html_text = f.read()
#     return render_template("songNew.html", lyrics=html_text)

# @app.route('/getTableData', methods=['GET', 'POST'])
def getSong(book:str, songnum:str, batch = 0) -> dict:
    """
    Retrieves a song from a JSON file based on the provided book and song number. The options are 'old', 'new', 'redergaran', and 'wordsongsindex'.

    Args:
        book (str): The book from which to retrieve the song.
        songnum (str): The number of the song to retrieve.
        batch (int, optional): The batch number. Defaults to 0.

    Returns:
        dict: A dictionary containing the song data.
    """
    if batch == 0:
        from json import load
        if book.lower() == "old" or book.lower() == "wordsongsindex":
            with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
                wordSongs = load(f)["SongNum"]
                return wordSongs[songnum]
        else:
            with open("REDergaran.json", 'r', encoding='utf-8') as f:
                REDergaran = load(f)["SongNum"]
                return REDergaran[songnum]
    else:
        pass

@app.route('/search/<searchLyrics>', methods=['GET'])
def songSearch(searchLyrics) -> list:
    """
    Searches for songs based on provided lyrics and returns a list of search results.

    Args:
        searchLyrics (str): The lyrics to search for in the songs.

    Returns:
        list: A list of search results, where each result is a dictionary containing the book, song number, and title of the song.
    """

    if searchLyrics:        
        query = {
            "$search": {
                "index": "search_index",
                "compound": {
                    "should": [
                        {
                            "text": {
                                "query": searchLyrics,
                                "path": "lyrics",
                                "fuzzy": {
                                    "maxEdits": 2,
                                    "prefixLength": 3
                                }
                            }
                        },
                        {
                            "phrase": {
                                "query": searchLyrics,
                                "path": "lyrics",
                                "slop": 0
                            }
                        }
                    ]
                }
            }
        }
        # results = songDB.aggregate([query, {"$limit": 10}])
        results = lyric_search_engine.main(searchLyrics)
        searchResults = []
 
    
        for result in results:
        
            if result[0].lower() == 'old':
                with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
                    index = json.load(f)
            else:
                with open('REDergaran.json', 'r', encoding='utf-8') as f:
                    index = json.load(f) 
            
            title = index['SongNum'][result[1]]['Title']
            
            title = title.split('\n')[0]
            
            
            
            searchResults.append(
                f'''<a class="list-group-item list-group-item-action" href="{url_for('display_song',book=result[0],songnum=result[1])}">{result[1]}: {title}</a>'''
            )

        return json.dumps(searchResults)

@app.route('/song/<book>/<songnum>', methods=['GET','POST'])
def display_song(book, songnum) -> str:
    """
    This function handles HTTP requests to the '/song/<book>/<songnum>' route.
    
    It takes two parameters: 'book' and 'songnum', which are used to identify a specific song.
    
    The function returns a rendered HTML template ('song.html') with the song's lyrics, 
    past songs, and similar songs.
    
    Parameters:
    book (str): The book identifier for the song (e.g., 'Old' or 'New').
    songnum (str): The song number identifier.
    
    Returns:
    A rendered HTML template with the song's lyrics, past songs, and similar songs.
    """
    from scanningDir import songSearch
    with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
        wordSongsIndex = json.load(f)

    with open('REDergaran.json', 'r', encoding='utf-8') as f:
        REDergaran = json.load(f)
    
    with open('song_occurrences.json', 'r', encoding='utf-8') as f:
        occr = json.load(f)
    
    book = book.lower()
    if book == 'wordsongsindex' or book == 'old':
        book = 'Old'
    else:
        book = 'New'
    past_songs = songSearch(songnum, book)
    similar_songs = None
    if songnum in occr[book]:
        similar_songs = occr[book][songnum]
    
    # template = f'''<a class="list-group-item list-group-item-action" href="{url_for('display_song',book=book,songnum=songnum)}">{songnum}: {title}</a>'''
    if past_songs != None:
        for songs in past_songs:
            song_titles = []
            for song_pair in songs['songs']:
                if not (None in song_pair):
                    # each song is a tuple ie: ('Old', '495')
                    # here I am simply adding a tuple(list(title))
                    title = ""
                    if song_pair[0] == 'Old':
                        if song_pair[1] in wordSongsIndex['SongNum']:
                            title = wordSongsIndex['SongNum'][song_pair[1]]["Title"]
                            title = title.split('\n')[0]
                    else:
                        if song_pair[1] in REDergaran['SongNum']:
                            title = REDergaran['SongNum'][song_pair[1]]["Title"]#REDergaran.get(['SongNum'][song_pair[1]]["Title"],None) # doing this to try to account for unusual song nums such as '32121'
                            title = title.split('\n')[0]
                    song_titles.append(f'''<a class="list-group-item list-group-item-action" href="{url_for('display_song',book=song_pair[0],songnum=song_pair[1])}">{song_pair[1]}: {title}</a>''')
            songs['songs'] = song_titles
    if similar_songs != None:
        song_titles = []
        for song_pair in similar_songs:
            # print(song_pair)
            song_pair = tuple(eval(song_pair))
            # print(song_pair)
            if not (None in song_pair):
                title = ""
                if song_pair[0] == 'Old':
                    if song_pair[1] in wordSongsIndex['SongNum']:
                        title = wordSongsIndex['SongNum'][song_pair[1]]["Title"]
                        title = title.split('\n')[0]
                else:
                    if song_pair[1] in REDergaran['SongNum']:
                        title = REDergaran['SongNum'][song_pair[1]]["Title"]#REDergaran.get(['SongNum'][song_pair[1]]["Title"],None) # doing this to try to account for unusual song nums such as '32121'
                        title = title.split('\n')[0]
                song_titles.append(f'''<a class="list-group-item list-group-item-action" href="{url_for('display_song',book=song_pair[0],songnum=song_pair[1])}">{song_pair[1]}: {title}</a>''')
        similar_songs = song_titles
        # print(similar_songs)
    
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as exec:
        future = exec.submit(openWord,songnum,book)
        lyrics = future.result()
        
    return render_template('song.html', lyrics=lyrics, past_songs=past_songs, similar_songs=similar_songs)

@app.route('/song/docx/<WordDoc>', methods=['GET','POST'])
def ServiceSongOpen(WordDoc) -> str: #Todo: come up with a better name
    """
    Renders the song.html template with lyrics from a .docx file.

    Parameters:
    WordDoc (str): The name of the .docx file.

    Returns:
    str: The rendered song.html template with lyrics.

    Notes:
    - If the .docx file exists in the htmlsongs directory, it reads the lyrics from the file.
    - If the .docx file does not exist, it attempts to open the file from the OneDrive path and save the lyrics as an html file.
    - If the file does not exist and cannot be opened, it flashes an error message.
    """
    if '.docx' in WordDoc:
        from glob import glob
        foundFiles = glob("htmlsongs\\"+WordDoc+"*")
        if foundFiles:
            # print(foundFiles)
            with open(foundFiles[0], 'r', encoding='utf-8') as f:
                lyrics = f.read()
            return render_template("song.html", lyrics = lyrics)
        else:
            with open("songs.json" , 'r', encoding='utf-8') as f:
                songs = json.load(f)
            songPth = songs[WordDoc]['path']
            songPth = songPth.split("OneDrive")[1] # bc of the way it's saved ie C:\Users\moses\OneDrive\Երգեր\06.2024\06.25.24.docx
            onedrive = env.get("OneDrive")
            songPth = onedrive+songPth
            print(songPth)
            # songPth = fr"{onedrive}\Երգեր\Պենտեկոստե\2024\2024 Պենտեկոստե.docx"
            import threading as th
            # MS_WORD = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
            wordDocThread = th.Thread(target=saveHtml,args=[songPth,WordDoc])#, args=[MS_WORD, songPth])
            wordDocThread.start()
            from time import sleep
            sleep(0.75)
            # saveHtml()
            with open(f"htmlsongs\\{WordDoc}.txt", 'r', encoding='utf-8') as f:
                html_text = f.read()
            return render_template("song.html", lyrics=html_text)
    else:
        flash("That song does not exist",'error')

@app.route('/song/<book>/<songnum>/attributes', methods=['GET','POST'])
def getSongAttributes(book,songnum) -> dict:
    """
    Handles HTTP requests to retrieve song attributes.

    Parameters:
        book (str): The book from which the song is retrieved.
        songnum (str): The song number within the book.

    Returns:
        A JSON response containing the song attributes.
    """
    return jsonify(getSong(book, songnum))

@app.route('/attributeSearch', methods=['GET','POST'])
def attributeSearch() -> dict:
    """This inputs a list of attributes and the finds songs whose attributes match the input attributes.
    
    Input:
        dict: A list of attributes
        ex:
        songattrs = {
            "Comments": "Dance-P5-5",
            "Title": "Եղբայրնե՛ր, ցնծացե՛ք",
            "Worship_Song": "",
            "key": "Em",
            "latestVersion": "Երգարան Word Files/1 Եղբայրնե՛ր, ցնծացե՛ք.docx",
            "opening_Song": "",
            "song_type": "Opening Song",
            "speed": "105",
            "style": "Disco",
            "timeSig": "4/4",
            "v1": "Երգարան Word Files/1 Եղբայրնե՛ր, ցնծացե՛ք.docx"
        }
        attributes = {key: true, speed: true, style: false, song_type: false, timeSig: true}
        
        dict: A list of song attributes
    
    Returns:
        dict: A dictionary where the keys are the song numbers and the values are the dictionaries of the respective songs

    """
    data = request.get_json()
    attributes = data["attributes"]
    songattrs = data["songattrs"]
    # print("Songattrs:",songattrs)
    # print("attributes:",attributes)
    if songattrs.get("Comments", None):
        del songattrs["Comments"]
    if songattrs.get("Title", None):
        del songattrs["Title"]
    
    temp = {}
    for attribute in songattrs:
        if attributes.get(attribute):#Check if the attribute is in the dictionary
            if attributes[attribute]:
                temp[attribute] = songattrs[attribute]
    songattrs = temp
    # print(songattrs)
    from json import load
    with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
        wordSongs = load(f)["SongNum"]
    
    with open("REDergaran.json", 'r', encoding='utf-8') as f:
        REDergaran = load(f)["SongNum"]
    returnSongs = {}
    returnSongs["WordSongsIndex"] = {}
    returnSongs["REDergaran"] = {}
    def filter_songs(songs):
        found_songs = {}
        for songNum, song in songs.items():
            matched =True
            for attr in songattrs:
                foundSongAttr = song.get(attr)
                if foundSongAttr != songattrs[attr]: matched = False
            
            if matched:
                found_songs[songNum] = song

        return found_songs
                
    # Filter songs from both sources
    returnSongs["WordSongsIndex"] =filter_songs(wordSongs)
    returnSongs["REDergaran"]=filter_songs(REDergaran)
    return jsonify(returnSongs)

            
def get_my_ip() -> str:
    """
    Retrieves the public IP address of the device making the request.
    
    Returns:
        str: The public IP address as a string.
    """
    from requests import get

    ip = get('https://api.ipify.org').content.decode('utf8')
    print('My public IP address is: {}'.format(ip))
    return ip

@app.route('/', methods=['GET', 'POST'])
def temp_home():
    """
    Handles HTTP requests to the root URL ('/').

    This function is responsible for handling both GET and POST requests. It checks for user sessions, 
    handles search queries, and returns relevant table data in JSON format or renders a blank HTML template if no user is logged in.

    Parameters:
    None

    Returns:
    A JSON response containing search results or a rendered HTML template.
    """
    # print(request.remote_addr,get_my_ip())
    if session.get('user', None):
        if session['user'] == 'local'or isUserAllowed(session['user']['userinfo']['email']):
            # data = request.get_json()
            table_data = None # doing this so that it does not get referenced before assginment
            book = request.args.get('book', None)
            if request.method == 'POST':
                from scanningDir import songChecker
                data = request.get_json(silent=True)
                if data:
                    query = data['query']
                    attribute = data['attribute']
                    book = data['book']
                    print(query)
                
                if attribute == 'Full_Text':
                    song_order = []
                    song_lyrics = lyric_search_engine.load_json_data('AllLyrics.json')
                    table_data = {}
                    links = json.loads(songSearch(query)) # returns a list of links ex: <a class="list-group-item list-group-item-action" href="/song/New/300">300: Օրհնյալ Սուրբ Հոգի, մեծ Մխիթարիչ,</a>
                    from re import findall
                    for link in links:
                        book = findall('/song/(.*?)/', link)[0]
                        song_num = findall(r'\d+', link)[0]
                        table_data[song_num] = getSong(book, song_num)
                        table_data[song_num]["book"] = book
                        lyrics = song_lyrics[book][song_num]
                        table_data[song_num]['lyrics'] = lyrics[:100]
                        song_order.append(song_num)
                    # print(table_data)
                        
                    # print(links)
                    # return json.dumps(links)
                    return json.dumps([table_data,song_order])
                
                if book and attribute and not query:
                    # print(load_table_data(book=book))
                    return json.dumps([load_table_data(book=book)])
                
                if query and book and attribute: # if attr is full_text
                    table_data = load_table_data(book=book)
                    query = query.lower()
                    filtered_data = {}
                    for song_num, attr in table_data.items():
                        if attribute == 'all':
                            # Search in all attributes
                            if any(query in str(val).lower() for val in attr.values()):
                                filtered_data[song_num] = attr
                        elif attribute in attr:
                            # Search only in the specified attribute
                            if query in str(attr[attribute]).lower():
                                filtered_data[song_num] = attr
                    # TODO: Find a more efficient/less computationally expensivse route than this for the latest date sang on
                    # for song_num in filtered_data:
                    #     last_sang_on = songChecker(book=filtered_data[song_num]['book'], songNum=song_num, three_month_window=False)
                    #     filtered_data[song_num]["last_sang_on"] = 
                    table_data = filtered_data
                    return json.dumps(table_data)
                
                elif not book:
                    flash('No book selected','warning') #practically not needed anymore
            
            # return render_template('index.html', table_data = table_data, book=book) #returns book, for continuity purposes
            return render_template('index.html', table_data = table_data, book=book) #returns book, for continuity purposes
        else:
            return redirect('logout')
    elif request.remote_addr == get_my_ip():
        session['user'] = 'local'
        return redirect('/')
    return render_template('index.html')

@app.route('/editsongs', methods=['GET', 'POST'])
def edit_songs():
    """
    Handles HTTP requests to the '/editsongs' route, allowing users to edit song information.
    
    If the request method is 'POST', it retrieves the song number and book from the request form,
    updates the song information based on the user's input, and saves the changes to a JSON file.
    
    The function returns a rendered template of the 'edit_songs.html' page, passing the updated song information and current values as parameters.
    
    Parameters:
    None
    
    Returns:
    A rendered template of the 'edit_songs.html' page
    """
    song_info = None
    current_values = None
    is_found = False
    if request.method == 'POST':
        
        song_num = request.form.get('songNum')
        book = request.form.get('book')
        # Bool_Lyrics = request.form.get('lyrics', False)
        
        # if Bool_Lyrics:
        #     return render_template('song.html', lyrics = openWord(song_num, book), book=book) #sending the book var inorder for the back button to function properly
        
        with open(f'{book}.json',encoding='utf-8') as f:
            data = json.load(f)
        
        songs = data.get('SongNum')  # Get the songs under the "SongNum" key
        song_info = songs.get(song_num)
        
        if song_info:
            # Save the current values before they are edited
            current_values = song_info.copy()
            if not current_values:
                flash("That song does not exist",'error')
        # else:
        #     flash("That song does not exist")
            
        if request.form.get('edit'):
            song_info['key'] = request.form.get('key')
            song_info['speed'] = request.form.get('speed')
            song_info['style'] = request.form.get('style')
            song_info['song_type'] = request.form.get('Song Type')
            # song_info['Worship_Song'] = request.form.get('Worship_Song')
            song_info['timeSig'] = request.form.get('Time Signature')
            song_info['Comments'] = request.form.get('Comments')
            songs["SongNum"] = song_info
            # with open(f'{book}.json', 'w', encoding='utf-8') as f:  # Save the changes to the same file
            #     json.dump(songs, f, indent=4, ensure_ascii=False)  # Write the whole data back to the file
        
        if request.form.get('submit'):
            song_info['key'] = request.form.get('key')
            song_info['speed'] = request.form.get('speed')
            song_info['style'] = request.form.get('style')
            song_info['song_type'] = request.form.get('Song Type')
            # song_info['Worship_Song'] = request.form.get('Worship_Song')
            song_info['timeSig'] = request.form.get('Time Signature')
            song_info['Comments'] = request.form.get('Comments')
            songs[song_num] = song_info
            # if song_info:
            #     return flash("That song does not exist",'error')
        with open(f'{book}.json', 'w', encoding='utf-8') as f:  # Save the changes to the same file
                json.dump(data, f, indent=4, ensure_ascii=False)  # Write the whole data back to the file
            
    return render_template('edit_songs.html', song_info=song_info, current_values=current_values) #add pretty=json.dumps(session.get('user'), indent=4) for debuging auth

    # return render_template('edit_songs.html')

@app.route('/tsank', methods=['GET','POST'])
def tsank():
    """
    Handles HTTP requests to the '/tsank' route, supporting both GET and POST methods.
    
    Retrieves the 'temmas' value from the request form data and uses it to load a JSON file.
    
    If 'temmas' is not None, it extracts a number from the value, uses it to index into the loaded JSON data,
    and renders the 'temas.html' template with the selected data.
    
    If 'temmas' is None, it renders the 'tema.html' template with the original 'temmas' value and an empty list.
    
    Returns a rendered HTML template.
    """
    temma = request.form.get("temmas", None)
    temmalist = None
    if temma:#checks to make sure it is not none
        from re import findall
        temmaNumber = findall(r"\d+", temma)
        with open("templates/temmas_new.json", 'r', encoding='utf-8') as f:
            temmalist = json.load(f)
        temmalist = temmalist[int(temmaNumber[0])-1]
        return render_template('temas.html', temmalist=temmalist)
            
    return render_template("tema.html", temmas=temma,temmalist=temmalist)

@app.route('/tsank_a_z', methods=['GET','POST'])
def tsank_A_Z():
    """
    Handles HTTP requests to the '/tsank_a_z' endpoint, accepting both GET and POST methods.
    Returns the rendered 'tsank_A_Z.html' template.
    """
    return render_template('tsank_A_Z.html')

@app.route('/tsank_a_z/<book>/<letter>', methods=['GET','POST'])
def tsank_letter(book, letter):
    # lookup_table = ['Ա','Բ','Գ','Դ','Ե','Զ','Է','Ը','Թ','Ժ','Ի','Լ','Խ','Ծ','Կ','Հ','Ձ','Ղ','Ճ','Մ','Յ','Ն','Շ','Ո','Չ','Պ','Ջ','Ս','Վ','Տ','Ց','Ու','Փ','Ք','Եւ','Օ']
    # lookup_index = lookup_table.index(letter)
    with open('first_letter.json', 'r', encoding='utf-8') as f:
        first_letter = json.load(f)
    selected_letter = [first_letter[book][letter][songnum] for songnum in first_letter[book][letter]]
    # selected_letter = []
    # for songnum in first_letter[book][letter]:
    #     selected_letter.append(first_letter[book][letter][songnum])
    return render_template('tsank_letter.html', selected_letter = selected_letter)

@app.route('/past_songs', methods=['GET','POST'])
def check_past_songs():
    """
    Handles the '/past_songs' route, accepting both GET and POST requests.
    
    When a POST request is made, it retrieves the 'SongNumTuple' from the request form,
    parses it to extract the song number and book, and then uses these values to search
    for past songs. If past songs are found, it formats the song titles and redirects the
    user to the 'display_song' route. If no past songs are found, it renders the 
    'check_past_songs.html' template.
    
    Parameters:
    None
    
    Returns:
    A redirect response to the 'display_song' route or a rendered 'check_past_songs.html' template.
    """
    from scanningDir import songSearch
    SongNumTuple = request.form.get('SongNumTuple')
    if SongNumTuple:
        pair = SongNumTuple.split(', ') # Song Number: ${element.songNum}, Book: ${element.book}
        SongNum = pair[0].split(': ')[1]
        book = pair[1].split(': ')[1]
        with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
            wordSongsIndex = json.load(f)
    
        with open('REDergaran.json', 'r', encoding='utf-8') as f:
            REDergaran = json.load(f)
        
        past_songs = songSearch(SongNum, book)
        if past_songs != None:
            for songs in past_songs:
                song_titles = []
                for song_pair in songs['songs']:
                    if not (None in song_pair):
                        # each song is a tuple ie: ('Old', '495')
                        # here I am simply adding a tuple(list(title))
                        title = ""
                        if song_pair[0] == 'Old':
                            if song_pair[1] in wordSongsIndex['SongNum']:
                                title = wordSongsIndex['SongNum'][song_pair[1]]["Title"]
                                title = title.split('\n')[0]
                        else:
                            if song_pair[1] in REDergaran['SongNum']:
                                title = REDergaran['SongNum'][song_pair[1]]["Title"]#REDergaran.get(['SongNum'][song_pair[1]]["Title"],None) # doing this to try to account for unusual song nums such as '32121'
                                title = title.split('\n')[0]
                        song_titles.append(f'''<a class="list-group-item list-group-item-action" href="{url_for('display_song',book=song_pair[0],songnum=song_pair[1])}">{song_pair[1]}: {title}</a>''')
                songs['songs'] = song_titles
        # return render_template('song.html', lyrics = openWord(SongNum, book), past_songs = past_songs)
        return redirect(url_for('display_song'), book=book,songnum=SongNum)#, title=title) #sending the book var inorder for the back button to function properly
    return render_template('check_past_songs.html')

#helper function for check_past_songs(), used with fetch api
@app.route('/past_songs/<songnum>', methods=['GET','POST'])
def past_songs(songnum):
    """
    Handles HTTP requests to the '/past_songs/<songnum>' route. 
    This function takes a song number and book as input, 
    searches for past songs matching the given song number and book, 
    and returns a rendered template with the past songs data.

    Parameters:
        songnum (str): The song number to search for past songs.

    Returns:
        A rendered HTML template with the past songs data.
    """
    past_songs = None
    SongNum = songnum
    data = request.get_json()
    book = data['book']
    # load the song database
    with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
        wordSongsIndex = json.load(f)
    with open('REDergaran.json', 'r', encoding='utf-8') as f:
        REDergaran = json.load(f)
    
    from scanningDir import songSearch
    past_songs = songSearch(SongNum, book)
    if past_songs != None:
        for songs in past_songs:
            song_titles = []
            for song_pair in songs['songs']:
                if not (None in song_pair):
                    title = ""
                    if song_pair[0] == 'Old':
                        if song_pair[1] in wordSongsIndex['SongNum']:
                            title = wordSongsIndex['SongNum'][song_pair[1]]["Title"]
                            title = title.split('\n')[0]
                    else:
                        if song_pair[1] in REDergaran['SongNum']:
                            title = REDergaran['SongNum'][song_pair[1]]["Title"]#REDergaran.get(['SongNum'][song_pair[1]]["Title"],None) # doing this to try to account for unusual song nums such as '32121'
                            title = title.split('\n')[0]
                    song_titles.append(f'''<a class="list-group-item list-group-item-action" href="{url_for('display_song',book=song_pair[0],songnum=song_pair[1])}">{song_pair[1]}: {title}</a>''')
            songs['songs'] = song_titles
            
    return render_template('pastsongtemplate.html', past_songs=past_songs)

@app.route('/newSundaySong', methods=['GET', 'POST'])
def newSundaySong():
    if request.method == 'POST':
        data = request.get_json()
        only_first_two_songs = data['only_first_two_songs']
        only_worship_songs = data['only_worship_songs']
        only_last_two_songs = data['only_last_two_songs']
        from song_curator import find_sunday_song
        reccomened_songs = find_sunday_song(only_first_two_songs, only_worship_songs, only_last_two_songs)
        
        return jsonify(reccomened_songs) if reccomened_songs else jsonify(None)
    return render_template('newSundaySongs.html')

@app.route('/weekdaySong', methods=['GET', 'POST'])
def weekdaySong():
    if request.method == 'POST':
        from song_curator import find_weekday_songs
        reccomened_songs = find_weekday_songs()
        return jsonify(reccomened_songs)
    return render_template('newWeekdaySongs.html')

@app.route('/transliterate', methods=['GET'])
def transliterate():
    session['transliterate'] = True
    return render_template('transliterate.html')

@app.route('/song/<book>/<songnum>/lyrics', methods=['GET','POST'])
def get_song_lyrics(book,songnum):
    if request.method == 'POST':
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as exec:
            future = exec.submit(openWord,songnum,book)
            lyrics = future.result()
        return jsonify(lyrics)
    return jsonify(None)

@app.route('/known_songs', methods=['GET','POST'])
def known_songs():
    # if request.method == "POST":
    #     #Begin writing to the dict
    #     pass
    return render_template('known_songs.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=env.get("PORT", 5000))
