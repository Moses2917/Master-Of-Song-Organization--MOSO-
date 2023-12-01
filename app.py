# app.py
from flask import Flask, render_template, request
import json

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
            song_info['opening_Song'] = request.form.get('opening_Song')
            song_info['Worship_Song'] = request.form.get('Worship_Song')
            song_info['timeSig'] = request.form.get('Time Signature')
            song_info['Comments'] = request.form.get('Comments')
            songs["SongNum"] = song_info
            # with open(f'{book}.json', 'w', encoding='utf-8') as f:  # Save the changes to the same file
            #     json.dump(songs, f, indent=4, ensure_ascii=False)  # Write the whole data back to the file
        if request.form.get('submit'):
            song_info['key'] = request.form.get('key')
            song_info['speed'] = request.form.get('speed')
            song_info['style'] = request.form.get('style')
            song_info['opening_Song'] = request.form.get('opening_Song')
            song_info['Worship_Song'] = request.form.get('Worship_Song')
            song_info['timeSig'] = request.form.get('Time Signature')
            song_info['Comments'] = request.form.get('Comments')
            songs[song_num] = song_info
        with open(f'{book}.json', 'w', encoding='utf-8') as f:  # Save the changes to the same file
            json.dump(data, f, indent=4, ensure_ascii=False)  # Write the whole data back to the file

    return render_template('song_info.html', song_info=song_info, current_values=current_values)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
