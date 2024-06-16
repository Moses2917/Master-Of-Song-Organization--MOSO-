def make_links():
    template = '''<a href="{{url_for('tsank_letter', letter=f"{letter}")}}">f"{letter}"</a>'''
    letters = "Ա Բ Գ Դ Ե Զ Է Ը Թ Ժ Ի Լ Խ Ծ Կ Հ Ձ Ղ Ճ Մ Յ Ն Շ Ո Չ Պ Ջ Ս Վ Տ Ց Ու Փ Ք Եւ Օ".split(" ")

    for letter in letters:
        print(f'''<a href="{{{{url_for('tsank_letter', letter='{letter}')}}}}">{letter}</a>''')
        if letter == "Խ" or letter == "Պ":
            print('<br>')

def make_tsank_letters(text_file_name='a-z.txt'):
    """inputs a txt file a-z.txt, and outputs 'starting_with_letter.txt'

    Args:
        text_file_name (_type_): _description_
        last_songnum (_type_): _description_
        save_filename (_type_): _description_
    """
    import json
    import re
    a_z = []
    lookup_table = ['Ա','Բ','Գ','Դ','Ե','Զ','Է','Ը','Թ','Ժ','Ի','Լ','Խ','Ծ','Կ','Հ','Ձ','Ղ','Ճ','Մ','Յ','Ն','Շ','Ո','Չ','Պ','Ջ','Ս','Վ','Տ','Ց','Ու','Փ','Ք','Եւ','Օ']
    with open('first_letter.json', 'r', encoding='utf-8') as f:
        starting_with_letter = json.load(f)
    starting_with_letter['New'] = {}
    for letter in lookup_table:
        starting_with_letter['New'][letter] = {}
    with open(text_file_name, "r", encoding='utf-8') as f:
        lines = f.read().split("\n")#re.sub("\n",'',f.read())
        for line in lines:
            if len(line) < 3 and line != '': # for getting the first line, works bc AHQ alr did this so I just need to read the first line
                if line == 'Ա': 
                    letter = line
                else:
                    if starting_with_letter:
                        letter = line
                # print(letter, starting_with_letter['New'][letter])
            
            # print("Songnum:",re.findall(r'[0-9]+',line[-5:])) 
            # print("Title:", re.findall(r'^[^.]+',line))
            Songnum = re.findall(r'[0-9]+',line[-5:])
            if len(Songnum) > 0: #to filter out empty lines
                title = re.findall(r'^[^.]+',line)
                # starting_with_letter.append(f'''{title[0]}: {{{{url_for('display_song',book='New',songnum={Songnum[0]})}}}}''')
                
                # starting_with_letter.append(f'''<a class="btn btn-primary" href="url_for('display_song',book='New',songnum={Songnum[0]})">{title[0]}</a><br>''')
                starting_with_letter['New'][letter][Songnum[0]]=f'''<a class="btn btn-dark shadow border border-light-subtle rounded-3 fs-5" href="/song/New/{Songnum[0]}">{title[0]}</a>'''

    with open('first_letter.json', 'w', encoding='utf-8') as f:
        json.dump(starting_with_letter,f,ensure_ascii=False,indent=4)

# make_tsank_letters()

def radixsort_arm_letters(nums, lookup_table):
    # max_length = max(len(num) for num in nums)
    max_length = 4
    lookup_dict = {char: idx for idx, char in enumerate(lookup_table)}

    for position in range(max_length - 1, -1, -1):
        # Create buckets for each character in the lookup table plus one for shorter strings
        buckets = [[] for _ in range(len(lookup_table) + 1)]

        for num in nums:
            # If the position is out of bounds for the current string, use the "extra" bucket
            if position >= len(num):
                buckets[-1].append(num)
            else:
                char = num[position]
                try:
                    index = lookup_dict[char.upper()]
                except:
                    print(char)
                buckets[index].append(num)

        # Flatten the list of buckets back into the original list
        nums = [item for sublist in buckets for item in sublist]

    return nums

    
def sort_oldbook_titles():
    with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
        import json
        word_songs = json.load(f)

    lookup_table = ['Ա','Բ','Գ','Դ','Ե','Զ','Է','Ը','Թ','Ժ','Ի','Լ','Խ','Ծ','Կ','Հ','Ձ','Ղ','Ճ','Մ','Յ','Ն','Շ','Ո','Չ','Պ','Ջ','Ս','Վ','Տ','Ց','Ու','Փ','Ք','ԵՎ','Օ']
    nums = ['ԴԱ', 'ԲԱ', 'ԳԱ', 'ԱԱ', 'ԵԱ', 'ԵՎԱ', 'ևԱ']

    # sorted_nums = radixsort_arm_letters(nums, lookup_table)
    # print(sorted_nums)  # Output should be the sorted list

    titles = []
    import re
    for songnum in word_songs["SongNum"]:
        title = word_songs["SongNum"][songnum]["Title"]
        # if '\n' in title:
        if len(title) > 2:
            title = title.split('\n')[0]
            print('\nbefore:', title)
            title = re.findall(r'[\D]+',title)[0] #get rid of all nums
            title = re.sub(r',','',title) #get rid of all dots ie: '.'
            title = re.sub(r'[.]+','',title) #get rid of all dots ie: '.'
            title = re.sub(r':','',title) #get rid of all dots ie: '.'
            title = re.sub(r'[(]','',title) #get rid of all dots ie: '.'
            # title = re.findall(r'[\w\s]+',title)[0] #get rid of all dots ie: '.'
            titles.append(title)
            print('\nafter:', title)
        
        

    # print(titles)
    sorted_titles = radixsort_arm_letters(titles, lookup_table)
    print(sorted_titles)
    # with open('sorted_wordSongIndex_titles.txt', 'w', encoding='utf-8') as f: # I could adjust the code or, be lazy and save as txt
    #     for x in sorted_titles:
    #         f.write(x + '\n')
def wrdindex_firstletter():
        
    with open('sorted_wordSongIndex_titles.txt', 'r', encoding='utf-8') as f:
        sorted_songs = f.read().split('\n')
    with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
        import json
        word_songs = json.load(f)
    lookup_table = ['Ա','Բ','Գ','Դ','Ե','Զ','Է','Ը','Թ','Ժ','Ի','Լ','Խ','Ծ','Կ','Հ','Ձ','Ղ','Ճ','Մ','Յ','Ն','Շ','Ո','Չ','Պ','Ջ','Ս','Վ','Տ','Ց','Ու','Փ','Ք','Եւ','Օ']

    import re
    sorted_songs_wth_songnum = []
    starting_with_letter = {}
    starting_with_letter['Old'] = {}
    for letter in lookup_table:
        starting_with_letter['Old'][letter] = {}
    for song_title in sorted_songs:
        for songnum in word_songs["SongNum"]: # just to find the song num of a title using the index
            title = word_songs["SongNum"][songnum]['Title']
            title = title.split('\n')[0]
            # print('\nbefore:', title)
            # try:
            if len(title) > 2:
                title = re.findall(r'[\D]+',title)[0] #get rid of all nums
                title = re.sub(r',','',title) #get rid of all dots ie: '.'
                title = re.sub(r'[.]+','',title) #get rid of all dots ie: '.'
                title = re.sub(r':','',title) #get rid of all dots ie: '.'
                title = re.sub(r'[(]','',title) #get rid of all dots ie: '.'
            if song_title in title:
                num = songnum
        
        if len(song_title) > 2:
            letter = song_title[0].upper()
            if letter == 'Ո'or letter == 'Ե':
                if song_title[1].lower() == 'ւ' or song_title[1].lower() =='վ':
                    letter = song_title[0]+'ւ'#song_title[0:2].lower()
            # print('\nletter:', letter)   
            sorted_songs_wth_songnum.append(song_title + ':' + num)
            print(num, song_title, letter)
            starting_with_letter['Old'][letter][num]=f'''<a class="btn btn-dark shadow border border-light-subtle rounded-3 fs-5" href="/song/Old/{num}">{song_title}</a>'''
    # starting_with_letter.pop()
    print(starting_with_letter)
    with open('first_letter.json', 'w', encoding='utf-8') as f:
        json.dump(starting_with_letter,f,ensure_ascii=False,indent=4)

    # titles = []
    # import re
    # for songnum in word_songs["SongNum"]:
    #     title = word_songs["SongNum"][songnum]["Title"]
    #     # if '\n' in title:
    #     if len(title) > 2:
    #         title = title.split('\n')[0]
    #         print('\nbefore:', title)
    #         title = re.findall(r'[\D]+',title)[0] #get rid of all nums
    #         title = re.sub(r',','',title) #get rid of all dots ie: '.'
    #         title = re.sub(r'[.]+','',title) #get rid of all dots ie: '.'
    #         title = re.sub(r':','',title) #get rid of all dots ie: '.'
    #         title = re.sub(r'[(]','',title) #get rid of all dots ie: '.'
    #         # title = re.findall(r'[\w\s]+',title)[0] #get rid of all dots ie: '.'
    #         titles.append(title)
    #         print('\nafter:', title)
            # letter = title[0]
            # if letter == 'Ո'or letter == 'Ե':
            #     if title[1].lower() == 'ւ':
            #         letter = title[0:2]
            
            # print('\nletter:', letter)


# with open('sorted_wordSongIndex_titles.txt', 'r', encoding='utf-8') as f:
#     sorted_songs = f.read().split('\n')
# with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
#     import json
#     word_songs = json.load(f)
# lookup_table = ['Ա','Բ','Գ','Դ','Ե','Զ','Է','Ը','Թ','Ժ','Ի','Լ','Խ','Ծ','Կ','Հ','Ձ','Ղ','Ճ','Մ','Յ','Ն','Շ','Ո','Չ','Պ','Ջ','Ս','Վ','Տ','Ց','Ու','Փ','Ք','Եւ','Օ']


# with open('first_letter.json', 'w', encoding='utf-8') as f:
#     json.dump(starting_with_letter,f,ensure_ascii=False,indent=4)