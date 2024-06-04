from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
#Setup mongodb
from pymongo import MongoClient

with open('{}\\Documents\\Code\\mongoPass.txt'.format(env.get("OneDrive")), 'r') as mongoPass:
    uri = "mongodb+srv://{}@cluster0.kgkoljn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(mongoPass.read()) #env.get('mongo_user')

# Create a new client and connect to the server
client = MongoClient(uri)
songDB = client.get_database("songs")
songDB = songDB.get_collection("allSongs")

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

# @app.route("/")
# def home():
#     return render_template("song_info.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

#This route is responsible for actually saving the session for the user, so when they visit again later, they won't have to sign back in all over again.
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

#the /login route, users will be redirected to Auth0 to begin the authentication flow.
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


#this route handles signing a user out from your application.
@app.route("/logout")
def logout():
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
    with open("{}\\Documents\\Code\\allowedEmails.csv".format(env.get("OneDrive")), 'r') as f:
        return email in f.read()

# Table data loading logic
def load_table_data(book):
    try:
        with open(f'{book}.json', mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data.get('SongNum')
    except FileNotFoundError:
        return None

def openWord(songNum, book):
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

@app.route('/', methods=['GET', 'POST'])
def song_info():
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

def saveHtml():
    from docx import Document

    songPth = r"C:\Users\Armne\OneDrive\Երգեր\Պենտեկոստե\2024\2024 Պենտեկոստե.docx"
    filePth = songPth  # find pth from index, and attach the location for onedrive
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
    with open(r"C:\Users\Armne\OneDrive\Documents\Code\Python\templates\songLyr.txt", 'w', encoding='utf-8') as f:
        f.write(html_text)

@app.route('/pentecost', methods=['GET'])
def DayofPentecost():
    import threading as th
    songPth = r"C:\Users\Armne\OneDrive\Երգեր\Պենտեկոստե\2024\2024 Պենտեկոստե.docx"
    MS_WORD = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
    wordDocThread = th.Thread(target=saveHtml)#, args=[MS_WORD, songPth])
    wordDocThread.start()
    # saveHtml()
    with open(r"C:\Users\Armne\OneDrive\Documents\Code\Python\templates\songLyr.txt", 'r', encoding='utf-8') as f:
        html_text = f.read()
    return render_template("songNew.html", lyrics=html_text)

@app.route('/search/<lyrics>', methods=['GET'])
def songSearch(lyrics):
    # lyrics = request.args.get('lyrics', None)
    #Looks for a song, given any lyric and return x(default of 10) search results

    if lyrics:

        query = {
            "$search": {
                "index": "search_index",
                "text": {
                    "query": lyrics,
                    "path": {
                        "wildcard": "*"
                    }
                }
            }
        }
        results = songDB.aggregate([query])
        searchResults = []
        
        
        
        n = 1
        for result in results:
            if n <= 10:
                if result['book'] == 'Old':
                    with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
                        index = json.load(f)
                else:
                    with open('REDergaran.json', 'r', encoding='utf-8') as f:
                        index = json.load(f) 
                
                title = index['SongNum'][result['songNum']]['Title']
                
                title = title.split('\n')[0]
                    
                searchResults.append({
                    # 'lyrics': result['lyrics'],
                    'book': result['book'],
                    'songNum': result['songNum'], # add a title var
                    'title': title
                })
            else:
                break
            n += 1

        return json.dumps(searchResults)

@app.route('/search', methods=['GET', 'POST'])
def searching():
    table_data = None
    book = request.form.get('book', None)
    SongNum = request.form.get('SongNum', None)
    SongNumTuple = request.form.get('SongNumTuple', None)
    SearchResultSong = request.form.get('SearchResultSong', None)
    # searchLyrics = request.args.get('searchLyrics', None)

    # if searchLyrics:
    #     return render_template('search.html', session=session.get('user'), table_data=table_data, words=songSearch(searchLyrics))

    if request.method == 'POST':
        
        if SearchResultSong:
            pair = SearchResultSong.split(', ') # Song Number: ${element.songNum}, Book: ${element.book}, Title: hkjh
            SongNum = pair[0].split(': ')[1]
            book = pair[1].split(': ')[1]
            # title = pair[2].split(': ')[1]
            return render_template('song.html', lyrics= openWord(SongNum, book))
        
        if (SongNum != None) or (SongNumTuple != None):
            from scanningDir import songSearch #used to search for past songs
            if SongNumTuple:
                pair = SongNumTuple.split(', ') # Song Number: ${element.songNum}, Book: ${element.book}
                SongNum = pair[0].split(': ')[1]
                book = pair[1].split(': ')[1]
                # book, SongNum = eval(SongNumTuple)
           
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
                            song_titles.append(song_pair + tuple([title]))
                    songs['songs'] = song_titles
            return render_template('song.html', lyrics = openWord(SongNum, book), book=book, past_songs = past_songs)#, title=title) #sending the book var inorder for the back button to function properly
        
        # Validate if book is selected
        if not book:
            return render_template('search.html', table_data= {})

        # Load table data based on the selected book
        table_data = load_table_data(book)

        if not table_data:
            return render_template('search.html', table_data=table_data, book=book,
                                message='No data found for the selected book.')  


    # Filter data based on search parameters
    query = request.form.get('query', '').lower()
    attribute = request.form.get('attribute', 'all')  # Default to 'all' if not specified

    if query:
        filtered_data = {}
        for song_num, attr in table_data.items():
            # Customize the search criteria based on your needs
            if attribute == 'all':
                # Search in all attributes
                if any(query in str(val).lower() for val in attr.values()):
                    filtered_data[song_num] = attr
            elif attribute in attr:
                # Search only in the specified attribute
                if query in str(attr[attribute]).lower():
                    filtered_data[song_num] = attr

        table_data = filtered_data

    return render_template('search.html', session=session.get('user'), table_data=table_data, book=book, query=query, attribute=attribute)

@app.route('/tsank', methods=['GET','POST'])
def tsank():
    book = request.form.get('book', None)
    temma = request.form.get("temmas", None)
    # table_data = {}
    table_data = None
    if book or temma:#checks to make sure it is not none
        if book == "REDergaran" or temma:
            temmalist = None
            if temma:
                from re import findall
                temmaNumber = findall(r"\d+", temma)
                with open("templates/temmas.json", 'r', encoding='utf-8') as f:
                    temmalist = json.load(f)
                temmalist = temmalist[int(temmaNumber[0])-1]
            return render_template("temmas.html", temmas=temma, temmalist=temmalist)#call a func. to get the list of songs
    return render_template("temma.html", session=session.get('user'),table_data=table_data,temmas=temma)

@app.route('/song', methods=['GET','POST'])
def display_song():
    return render_template('song.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=env.get("PORT", 5000))
