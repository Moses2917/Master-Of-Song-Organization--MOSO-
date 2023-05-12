from pytube import YouTube
# vid_url = input("Please input your video url: ")
vid_url = "https://youtu.be/RGtZq0W85JU"
yt = YouTube(vid_url)
def vidDownLoad(yt):
    filtered = yt.streams.filter(file_extension='mp4',res="1080p")
    print(filtered)
    print("itag=" + str(filtered[0].itag))
    input("Is this the correct stream?")
    stream = yt.streams.get_by_itag(filtered[0].itag)
    print("Now downloading stream")
    stream.download()

def audioDownload(yt):
    filtered = yt.streams.filter(only_audio=True)
    print(filtered)
    print("itag=" + str(filtered[0].itag))
    input("Is this the correct stream?")
    stream = yt.streams.get_by_itag(filtered[0].itag)
    stream.download()
    
# vidDownLoad(yt)

audioDownload(yt)