path = "templates/temmas.json"

with open(path,'r',encoding='utf-8') as f:
    from json import load
    temmas = load(f)
from re import findall
new_temma = []
for each in temmas:
    temma_list = each.split("<br>")
    temma_str = ""
    for tema in temma_list:
        # print(tema)
        song_num = findall(r'\d+',tema)[0]
        # print(f'<a class="btn btn-dark shadow border border-light-subtle rounded-3 fs-5" href="/song/New/{song_num}">{tema}</a>')
        temma_str += f'<a class="btn btn-dark shadow border border-light-subtle rounded-3 fs-5" href="/song/New/{song_num}">{tema}</a><br>'
    new_temma.append(temma_str)
with open("templates/temmas_new.json", 'w', encoding='utf-8') as f:
    from json import dump
    dump(new_temma,f,ensure_ascii=False)
        