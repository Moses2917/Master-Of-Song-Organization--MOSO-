def make_links():
    template = '''<a href="{{url_for('tsank_letter', letter=f"{letter}")}}">f"{letter}"</a>'''
    letters = "Ա Բ Գ Դ Ե Զ Է Ը Թ Ժ Ի Լ Խ Ծ Կ Հ Ձ Ղ Ճ Մ Յ Ն Շ Ո Չ Պ Ջ Ս Վ Տ Ց Ու Փ Ք Եւ Օ".split(" ")

    for letter in letters:
        print(f'''<a href="{{{{url_for('tsank_letter', letter='{letter}')}}}}">{letter}</a>''')
        if letter == "Խ" or letter == "Պ":
            print('<br>')

def make_tsank_letters():
    import json
    a_z = []
    starting_with_letter = []
    # template = f'{title}:{Songnum}'
    import re
    with open('a-z.txt', "r", encoding='utf-8') as f:
        lines = f.read().split("\n")#re.sub("\n",'',f.read())
        for line in lines:
            if len(line) < 3:
                if line == 'Ա': # for getting the first line
                    letter = line
                else:
                    if starting_with_letter:
                        a_z.append(starting_with_letter)
                        letter = line
                        starting_with_letter = []
            
            # print("Songnum:",re.findall(r'[0-9]+',line[-5:])) 
            # print("Title:", re.findall(r'^[^.]+',line))
            Songnum = re.findall(r'[0-9]+',line[-5:])
            if len(Songnum) > 0: #to filter out empty lines
                title = re.findall(r'^[^.]+',line)
                # starting_with_letter.append(f'''{title[0]}: {{{{url_for('display_song',book='New',songnum={Songnum[0]})}}}}''')
                
                # starting_with_letter.append(f'''<a class="btn btn-primary" href="url_for('display_song',book='New',songnum={Songnum[0]})">{title[0]}</a><br>''')
                starting_with_letter.append(f'''<a class="btn btn-dark shadow border border-light-subtle rounded-3 fs-5" href="/song/New/{Songnum[0]}">{title[0]}</a>''')
            
                if Songnum[0] == '935':
                    a_z.append(starting_with_letter)


    print(a_z)

    with open('starting_with_letter.txt', 'w', encoding='utf-8') as f:
        json.dump(a_z,f,ensure_ascii=False,indent=4)