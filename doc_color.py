import os
import re
from tracemalloc import start
from docx import Document
from docx import shared


def get_colored_text(filepath='', doc=None) -> dict:

    # Open the document
    if not doc:
        doc = Document(filepath)
    colored_text = {}
    # Access a specific paragraph (e.g., the first one)
    for paragraph in doc.paragraphs:
        # Iterate through runs in the paragraph to check their font colors
        for run in paragraph.runs:
            # Get the color format object
            color_format = run.font.color
            
            # if color_format.type is None:
            #     print(f'Text: "{run.text}", Color: None (default)')
            if hasattr(color_format, 'rgb') and color_format.rgb:
                # Get the RGB value
                rgb_value = color_format.rgb

                rgb_str = str(rgb_value)
                if rgb_str != "000000": # Only get colored text
                    colored_text[run.text] = rgb_str
    return colored_text


def get_all_colored_text(filepath='', doc=None) -> list[str]:
    """Returns a html code in a list of all text and includes color

    Args:
        filepath (str): The filepath of the doc file
        doc (document.Document, optional): The doc obj to use instead of filepath. Defaults to None.

    Returns:
        colored_text: list of lines of html code
    """

    # Open the document
    if not doc:
        doc = Document(filepath)
    # colored_text: list[tuple[str,str]] = []
    colored_text = []
    song_nums = []
    song_counter = 0
    start_song = False
    # Access a specific paragraph (e.g., the first one)
    for paragraph in doc.paragraphs:
        # Iterate through runs in the paragraph to check their font colors
        # A run is like a smaller paragraph, its more like an inline small group of words with common/similer characteristics
        # For each line we need a <p>
        buffer = ""
        #Next we need to add to the <p> element... then close it up
        if "Դու գիտես Տիրոջ պատվերները" in paragraph.text:
            ...
        if paragraph.text == '':
            colored_text.append("<br>")
        else:
            buffer += "<p>"
            
            for run in paragraph.runs:
                two_br = False # True if adding another br makes it two in a row
                text = run.text
                lines = text.split('\n')

                if len(lines) > 2 and line[0] == '' and line[1] == '':
                    buffer+="<br>"
                if start_song:
                    if song_counter != 1: # can't do buffer, buffer is like for a paragraph
                        colored_text.append(f'</div>')
                    colored_text.append(f'<div id=song-{song_counter}>')
                    song_nums.append(text)
                    start_song=False
                if "start" in text:
                    # Meets start song in this run, then the song num is imeadiately in the next run.
                    start_song = True
                    song_counter += 1

                text_color: None | shared.RGBColor = run.font.color.rgb # gets rgb values of text
                if bool(text_color) and str(text_color) != "000000" and "\n" not in text:
                    rgb = True
                    # use span bc its inline
                    buffer+=f"<span style= color:{text_color}>" # Here we can get the color/decide what color to apply
                for line in lines:
                    if line != '':
                        buffer+=line
                    else:
                        if not two_br:
                            two_br = True
                            buffer+="<br>"
                if rgb:
                    buffer+="</span>"
                    rgb = False
            buffer += "</p>"
            colored_text.append(buffer)

    return tuple([colored_text, song_nums])

if '__main__' == __name__:
    if os.name == "nt":
        filepath = r"C:\Users\moses\OneDrive\Երգեր\06.2025\06.01.25.docx"
    else:
        filepath = r"/Users/movsesmovsesyan/Library/CloudStorage/OneDrive-Personal/Երգեր/Պենտեկոստե/2025/Պենտեկոստե.docx"
    colored_text = get_all_colored_text(filepath)
    for line in colored_text[0]:
        print(line)
    
    print(colored_text[1])
    