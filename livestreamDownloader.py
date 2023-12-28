import pytube


vid_url = "https://www.youtube.com/live/sFpCaRTrcQI?si=FLITPCkjBqj5_x0c"
yt = YouTube(vid_url)
def vidDownLoad(yt):
    filtered = yt.streams.filter(file_extension='mp4',res="1080")
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
    
vidDownLoad(yt)

# audioDownload(yt)