from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
import json

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

@app.route('/', methods=['GET', 'POST'])
def song_info():
    song_info = None
    current_values = None
    if len(session) > 1:
        if isUserAllowed(session['user']['userinfo']['email']):
            
            if request.method == 'POST':
                song_num = request.form.get('songNum')
                book = request.form.get('book')
                with open(f'{book}.json',encoding='utf-8') as f:
                    data = json.load(f)
                songs = data.get('SongNum')  # Get the songs under the "SongNum" key
                song_info = songs.get(song_num)
                if song_info:
                    # Save the current values before they are edited
                    current_values = song_info.copy()
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
                with open(f'{book}.json', 'w', encoding='utf-8') as f:  # Save the changes to the same file
                    json.dump(data, f, indent=4, ensure_ascii=False)  # Write the whole data back to the file
                
            return render_template('song_info.html', session=session.get('user'), song_info=song_info, current_values=current_values) #add pretty=json.dumps(session.get('user'), indent=4) for debuging auth
        
        else:
            return redirect('logout')
    
    return render_template('song_info.html', session=session.get('user'))




@app.route('/search', methods=['GET', 'POST'])
def searching():
    table_data = {}
    book = request.form.get('book', '')

    if request.method == 'POST':
        # Validate if book is selected
        if not book:
            return render_template('search.html', table_data=table_data)

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
            return render_template("temma.html", temmas=temma, temmalist=temmalist)#call a func. to get the list of songs
    return render_template('tsank.html', session=session.get('user'),table_data=table_data,temmas=temma)


if __name__ == '__main__':
    #,ssl_context='adhoc'
    app.run(debug=True,host='0.0.0.0',port=env.get("PORT", 5000))
