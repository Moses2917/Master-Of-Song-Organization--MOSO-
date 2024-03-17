# app.py
from flask import Flask, render_template, request
import json, pandas
from os import environ

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def song_info():
    song_info = None
    current_values = None
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

    return render_template('song_info.html', song_info=song_info, current_values=current_values)

# @app.route('/search',  methods=['GET', 'POST'])
# def search():
#     table_data = {}
#     if request.method == 'POST':
#         book = request.form.get('book')
#         if book == None or book == "":
#             return render_template('search.html',table_data=table_data)
#         else:
#             table_data = json.load(open(f'{book}.json',mode='r',encoding='utf-8'))
#             table_data = table_data.get('SongNum')
#     return render_template('search.html',table_data=table_data)


# Table data loading logic
def load_table_data(book):
    try:
        with open(f'{book}.json', mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data.get('SongNum')
    except FileNotFoundError:
        return None


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

    return render_template('search.html', table_data=table_data, book=book, query=query, attribute=attribute)

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
    return render_template('tsank.html',table_data=table_data,temmas=temma)


if __name__ == '__main__':
    #,ssl_context='adhoc'
    app.run(debug=True,host='192.168.1.151')
