import os
import re
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


def get_all_colored_text(filepath, doc=None) -> list[tuple[str,str]]:

    # Open the document
    if not doc:
        doc = Document(filepath)
    # colored_text: list[tuple[str,str]] = []
    colored_text = []
    song_nums = []
    # Access a specific paragraph (e.g., the first one)
    for paragraph in doc.paragraphs:
        # Iterate through runs in the paragraph to check their font colors
        # A run is like a smaller paragraph, its more like an inline small group of words with common/similer characteristics
        # for run in paragraph.runs:
        #     # Get the color format object
        #     color_format = run.font.color
            
        #     # if color_format.type is None:
        #     #     print(f'Text: "{run.text}", Color: None (default)')
        #     if hasattr(color_format, 'rgb') and color_format.rgb:
        #         # Get the RGB value
        #         rgb_value = color_format.rgb
                
        #         # Convert to hex format using string representation
        #         # Since RGBColor appears to be implemented as RGBColor(0x3f, 0x2c, 0x36)
        #         rgb_str = str(rgb_value)
        #         colored_text.append((run.text, rgb_str))
        #         # if rgb_str != "000000": # Only get colored text
        #         #     colored_text[run.text] = rgb_str
                
        #         # If you need a hex string, you can extract from the representation:
        #         # if 'RGBColor' in rgb_str:
        #         #     try:
        #         #         # Parse values from the string representation
        #         #         values = rgb_str.replace('RGBColor(', '').replace(')', '').split(', ')
        #         #         if len(values) == 3:
        #         #             hex_color = f'#{int(values[0], 16):02x}{int(values[1], 16):02x}{int(values[2], 16):02x}'
        #         #             print(f'Hex color: {hex_color}')
        #         #     except Exception as e:
        #         #         print(f'Error parsing RGB string: {e}')
        #     else:
        #         colored_text.append((run.text, '000000'))
            
        # text = paragraph.text
        # if text != "":
        #     for line in text.split('\n'):# -> ["sadasd"] if no \n just returns the string in a list                
        #         print(f"<p>{line}</p>")
        # else:
        #     print("<br>")
        
        # each run is a group of words with the same properites
        # as a subset of a line/paragraph
        
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
                text = run.text
                lines = text.split('\n')
                if len(lines) > 2 and line[0] == '' and line[1] == '':
                    buffer+="<br>"
                    buffer-="<>"
                text_color: None | shared.RGBColor = run.font.color.rgb # gets rgb values of text
                if bool(text_color) and str(text_color) != "000000" and "\n" not in text:
                    rgb = True
                    # use span bc its inline
                    buffer+=f"<span style= color:{text_color}>" # Here we can get the color/decide what color to apply
                # if len(lines) < 1:
                #     if lines[0] == '' and lines[1] == '':
                #         print("<br>")
                # else:
                for line in lines:
                    if "բարձրացնելով քո փառքը" in line:
                        ...
                    if line != '':
                        buffer+=line
                    else:
                        buffer+="<br>"
                if rgb:
                    buffer+="</span>"
                    rgb = False
            buffer += "</p>"
            colored_text.append(buffer)
        # text = paragraph.text
        # if text != "":
        #     for line in text.split('\n'):# -> ["sadasd"] if no \n just returns the string in a list                
        #         print(f"<p>{line}</p>")
        # else:
        #     print("<br>")
        
        # print("<p>", end='')
        # for run in paragraph.runs: # Runs are in-line, so no \n
        #     text = run.text
        #     if text != "\n":
        #         lines = text.split('\n')
        #         # if "Դեպի Քեզ աղաղակել" in lines:
        #         #     ...
        #         if "Նորից կանչում եմ" in lines:
        #             ...
        #         for line in lines:# -> ["sadasd"] if no \n just returns the string in a list
        #             # print(f"<p>{line}</p>")
        #             if line != "":
        #                 print(line, end='')
        #             else:
        #                 print("</p>")
        #                 print("<p>", end='')
        #     else:
        #         print("</p>")
        #         print("<br>")
        # if text != "\n": print("</p>") # extra </p>, bc if \n then alr </p>
        # if paragraph.text == "":
        #     print("<br>")

    # print(colored_text)
    return colored_text

def convert_to_html(document):
    html_doc = []

if '__main__' == __name__:
    if os.name == "nt":
        filepath = r"C:\Users\moses\OneDrive\Երգեր\Պենտեկոստե\2025\Պենտեկոստե.docx"
    else:
        filepath = r"/Users/movsesmovsesyan/Library/CloudStorage/OneDrive-Personal/Երգեր/Պենտեկոստե/2025/Պենտեկոստե.docx"
    colored_text = get_all_colored_text(filepath)
    for line in colored_text:
        print(line)
    