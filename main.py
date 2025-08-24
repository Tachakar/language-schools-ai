import sys
import os
import pathlib
import googleapiclient.discovery
import yt_dlp
import whisper
import pprint

BASE_PATH = pathlib.Path('.')
AUDIO_PATH = BASE_PATH / 'audios'
TRANSCRIPT_PATH = BASE_PATH / 'transcripts'

YDL_OTPS = {
            "format": "bestaudio",
            "outtmpl": "audios/%(id)s.%(ext)s",
            "quiet":True,
            "download_archive": "downloaded.txt",
            "postprocessors": [{
                "key":"FFmpegExtractAudio",
                 "preferredcodec":"wav",
            }]
}

def check_path(path):
    if path.exists() == False or path.is_dir() == False:
        q = str(input(f"Do you want to create folder for {path.name}(Y/n)"))
        if q == "Y":
            path.mkdir()
            return True
        elif q == "n":
            print("Canceling installation")
            return False
        else:
            print("Something went wrong")
            return False

def pull_metadata() -> dict:
    try:
        youtube = googleapiclient.discovery.build(serviceName="youtube", version="v3", developerKey=os.environ.get("google_cloud_api_key"))
        req = youtube.search().list(
            part="snippet",
            maxResults=3,
            videoLicense="creativeCommon",
            q="english lessons",
            type="video",
            videoDuration="medium",
        )
        print("Metadata pulled")
        return req.execute()
    except Exception as e:
        print(f"Something went wrong while pulling metadata, ErrorMessage: {e}")
        return {}

def get_urls(data: dict) -> list:
    videos = data.get('items', None)
    if videos != None:
        urls = []
        for video in videos:
            id = video['id']['videoId']
            url = f"https://www.youtube.com/watch?v={id}"
            urls.append(url)
        print("Got urls")
        return urls
    print("Something went wrong in get_urls()")
    return []

def download_audios(urls: list) -> None:
    if check_path(path=AUDIO_PATH) == False:
        return
    with yt_dlp.YoutubeDL(YDL_OTPS) as ydl:
        ydl.download(urls)

def make_transcripts():
    if check_path(path=TRANSCRIPT_PATH) == False:
        return
    model = whisper.load_model(name='tiny.en')
    for wav_file in AUDIO_PATH.iterdir():
        result = model.transcribe(str(wav_file.absolute()))
        print(result["text"])
        return

if __name__ == "__main__":
    try:
        data = pull_metadata()
        urls = get_urls(data=data)
        download_audios(urls=urls)
        make_transcripts()
    except Exception as e:
        print(f"Something went wrong.\n{e}")
