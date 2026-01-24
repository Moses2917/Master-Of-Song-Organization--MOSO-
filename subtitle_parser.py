import datetime
import re,os,subprocess
import uuid # use for making names
root_folder = 'F:/dataset/raw_data'
output_folder = 'F:/dataset/prossed_audio/'
# Filter and clean up thr captions
def clean_captions(filepath):
    with open(filepath, 'r', encoding='utf-8') as srt:
        file = srt.read().split('\n')
    new_file = []
    for line in file:
        if line != '' and line != r"\n": new_file.append(line)
    # print(f"pre-filter # of captions: {len(new_file)//3}")
    step_size = 3
    caption_dict = {}
    for line in range(0, len(new_file), step_size):
    # srt_caption_chunk = new_file[line:line+step_size]
        caption_id, timedelta, text= new_file[line:line+step_size]
        text:str
    # Filter for only armenian text, and text that is at least two to three words, with no nums
        if len(text.split()) > 3 and not re.match('[0-9]+', text) and re.match(r'[Ա-Ֆա-ֆև]+', text):
            text = re.sub(r'[^Ա-Ֆա-ֆև\sun,՝՜՛,-:։,.]*', '', text)
        # Get the correct time delta, replacing , with . for ffmpeg
            timedelta = re.findall('[\d:.]+', timedelta.replace(',' , '.'))
            caption_dict[caption_id] = {}
            caption_dict[caption_id]['timedelta'] = timedelta
            caption_dict[caption_id]['text'] = text
    return caption_dict

def save_cap(caption_item, uuid):
    """Write the caption as a text file,
    Using the same UUID as the audio file.

    Args:
        caption_item (_type_): _description_
        uuid (_type_): _description_
    """
    with open(f"{output_folder}/{uuid}.txt", 'w', encoding='utf-8') as cap_file:
        cap_file.write(caption_item['text'])

def trim_cut(caption_item:dict, video_path:str, unique_name:str):
    """Call ffmpeg to trim and cut, save the out file and caption under the same file name

    Args:
        caption_item (dict): _description_
        video_path (str): _description_
    """
    in_time = datetime.datetime.strptime(caption_item['timedelta'][0],'%H:%M:%S.%f')
    end_time = datetime.datetime.strptime(caption_item['timedelta'][1],'%H:%M:%S.%f')
    time_diff: datetime.timedelta = end_time - in_time
    time_diff.total_seconds()
    args = f"ffmpeg -ss {caption_item['timedelta'][0]} -i \"{video_path}\" -t {time_diff.total_seconds()} -ar 16000 {output_folder}/{unique_name}.wav"
    print(args)
    subprocess.run(args=args, shell=True, text=True)
    save_cap(caption_item, unique_name)

for folder in os.listdir(root_folder):
    video_dir = os.listdir(f'{root_folder}/{folder}')
    # print(video_dir)
    if '.srt' in video_dir[0][-3:]:
        caption = video_dir[1]
        video = video_dir[0]
    else:
        caption = video_dir[0]
        video = video_dir[1]

    caption_dict = clean_captions(f'{root_folder}/{folder}/{caption}') # possibly need to swap u with ս
    for id, content in caption_dict.items():
        trim_cut(content, f'{root_folder}/{folder}/{video}', str(uuid.uuid4()))