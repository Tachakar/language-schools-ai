import sys
import os
import pathlib
import googleapiclient.discovery
import yt_dlp
import whisper

BASE_PATH = pathlib.Path('.')
AUDIO_PATH = BASE_PATH / 'audios'
TRANSCRIPT_PATH = BASE_PATH / 'transcripts'

YDL_OPTS = {
            "format": "bestaudio",
            "outtmpl": "audios/%(id)s.%(ext)s",
            "quiet":False,
            "download_archive": "downloaded.txt",
            "postprocessors": [{
                "key":"FFmpegExtractAudio",
                 "preferredcodec":"wav",
            }]
}

MAX_RESULTS = 3
VIDEO_LICENSE = "creativeCommon"
Q = "english lessons"
def check_api_key() -> None:
    if os.environ.get("YOUTUBE_API_KEY", None) == None:
        sys.exit("Coulnd't get youtube api key")

def check_path(path:pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def fetch_youtube_metadata() -> dict:
    try:
        youtube = googleapiclient.discovery.build(serviceName="youtube", version="v3", developerKey=os.environ.get("YOUTUBE_API_KEY"))
        req = youtube.search().list(
            part="snippet",
            maxResults=MAX_RESULTS,
            videoLicense=VIDEO_LICENSE,
            q=Q,
            type="video",
            videoDuration="medium",
        )
        print("Metadata pulled")
        return req.execute()
    except Exception as e:
        sys.exit(f"Something went wrong in fetch_api. Message: {e}")

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

def download_wav_files(urls: list) -> None:
    if urls == []:
        sys.exit("URLs list is empty")
    check_path(path=AUDIO_PATH)
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download(urls)

def make_transcripts():
    check_path(path=TRANSCRIPT_PATH)
    model = whisper.load_model(name='medium.en')
    for wav_file in AUDIO_PATH.iterdir():
        result = model.transcribe(str(wav_file.absolute()))
        print(result["text"])

if __name__ == "__main__":
    try:
        check_api_key()
        data = fetch_youtube_metadata()
        urls = get_urls(data=data)
        download_wav_files(urls=urls)
        make_transcripts()
    except Exception as e:
        print(f"Something went wrong.\n{e}")
