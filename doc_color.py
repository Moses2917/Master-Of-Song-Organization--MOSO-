from docx import Document

def get_colored_text(filepath) -> dict:

    # Open the document
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
                
                # Convert to hex format using string representation
                # Since RGBColor appears to be implemented as RGBColor(0x3f, 0x2c, 0x36)
                rgb_str = str(rgb_value)
                if rgb_str != "000000": # Only get colored text
                    # print(f'Text: "{run.text}", Color RGB: {rgb_str}')
                    colored_text[run.text] = rgb_str
                
                # If you need a hex string, you can extract from the representation:
                # if 'RGBColor' in rgb_str:
                #     try:
                #         # Parse values from the string representation
                #         values = rgb_str.replace('RGBColor(', '').replace(')', '').split(', ')
                #         if len(values) == 3:
                #             hex_color = f'#{int(values[0], 16):02x}{int(values[1], 16):02x}{int(values[2], 16):02x}'
                #             print(f'Hex color: {hex_color}')
                #     except Exception as e:
                #         print(f'Error parsing RGB string: {e}')
            
            # elif hasattr(color_format, 'theme_color') and color_format.theme_color:
            #     print(f'Text: "{run.text}", Theme color: {color_format.theme_color}')

    # print(colored_text)
    return colored_text

if '__main__' == __name__:
    print(get_colored_text(r"C:\Users\moses\OneDrive\Երգեր\Պենտեկոստե\2025\Պենտեկոստե.docx"))
    