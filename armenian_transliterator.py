def armenian_to_english():
    # Armenian to English transliteration mapping
    armenian_to_latin = {
        'ա': 'a', 'բ': 'b', 'գ': 'g', 'դ': 'd', 'ե': 'e', 'զ': 'z', 'է': 'e',
        'ը': '@', 'թ': 't', 'ժ': 'zh', 'ի': 'i', 'լ': 'l', 'խ': 'kh', 'ծ': 'ts',
        'կ': 'k', 'հ': 'h', 'ձ': 'dz', 'ղ': 'gh', 'ճ': 'ch', 'մ': 'm', 'յ': 'y',
        'ն': 'n', 'շ': 'sh', 'ո': 'o', 'չ': 'ch', 'պ': 'p', 'ջ': 'j', 'ռ': 'r',
        'ս': 's', 'վ': 'v', 'տ': 't', 'ր': 'r', 'ց': 'ts', 'ւ': 'v', 'փ': 'p',
        'ք': 'k', 'օ': 'o', 'ֆ': 'f', 'և': 'ev', 'ու': 'u',
        # Uppercase mappings
        'Ա': 'A', 'Բ': 'B', 'Գ': 'G', 'Դ': 'D', 'Ե': 'E', 'Զ': 'Z', 'Է': 'E',
        'Ը': '@', 'Թ': 'T', 'Ժ': 'Zh', 'Ի': 'I', 'Լ': 'L', 'Խ': 'Kh', 'Ծ': 'Ts',
        'Կ': 'K', 'Հ': 'H', 'Ձ': 'Dz', 'Ղ': 'Gh', 'Ճ': 'Ch', 'Մ': 'M', 'Յ': 'Y',
        'Ն': 'N', 'Շ': 'Sh', 'Ո': 'O', 'Չ': 'Ch', 'Պ': 'P', 'Ջ': 'J', 'Ռ': 'R',
        'Ս': 'S', 'Վ': 'V', 'Տ': 'T', 'Ր': 'R', 'Ց': 'Ts', 'Փ': 'P', 'Ք': 'K',
        'Օ': 'O', 'Ֆ': 'F'
    }
    return armenian_to_latin

def transliterate(text):
    mapping = armenian_to_english()
    result = ''
    i = 0
    while i < len(text):
        # Check for two-character combinations first
        if i < len(text) - 1 and text[i:i+2] in mapping:
            result += mapping[text[i:i+2]]
            i += 2
        # Then check for single characters
        elif text[i] in mapping:
            result += mapping[text[i]]
            i += 1
        # If character is not in mapping, keep it as is
        else:
            result += text[i]
            i += 1
    return result

# Example usage
if __name__ == "__main__":
    # Test cases
    test_cases = [
        "խնդրում եմ աղոթեք",  # khndrum em axoteq
        "Աստված օրհնի",       # Astvats orhni
        "Խաղաղություն"        # Khaxaxutyun
    ]
    
    print("Armenian to English Transliteration Examples:")
    for text in test_cases:
        print(f"Armenian: {text}")
        print(f"English:  {transliterate(text)}\n")

# Additional helper function to process multiple lines
def process_prayer_requests(text):
    lines = text.split('\n')
    transliterated_lines = []
    for line in lines:
        if line.strip():  # Skip empty lines
            transliterated_lines.append(transliterate(line))
    return '\n'.join(transliterated_lines)
