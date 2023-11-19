# app.py
from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def song_info():
    song_info = None
    if request.method == 'POST':
        song_num = request.form.get('songNum')
        book = request.form.get('book')
        with open(f'{book}.json',encoding='utf-8') as f:
            songs = json.load(f)
        song_info = songs.get(song_num)
        if request.form.get('edit'):
            song_info['key'] = request.form.get('key')
            song_info['speed/tempo'] = request.form.get('speed/tempo')
            song_info['style'] = request.form.get('style')
            song_info['opening_Song'] = request.form.get('opening_Song')
            song_info['Worship_Song'] = request.form.get('Worship_Song')
            songs[song_num] = song_info
            with open(f'path/to/your/json/{book}.json', 'w') as f:
                json.dump(songs, f)
    return render_template('song_info.html', song_info=song_info)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
