import sys
import os
import pathlib
import googleapiclient.discovery
import yt_dlp

BASE_PATH = pathlib.Path('.')

YDL_OTPS = {
            "format": "bestaudio",
            "outtmpl": "audios/%(id)s.%(ext)s",
            "quiet":True,
            "download_archive": "downloaded.txt",
            "postprocess": [{
                "key":"FFmpegExtractAudio",
                 "preferredcodec":"wav",
                 "prefferedquality":"192",
            }]
}

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
    AUDIO_PATH = BASE_PATH / 'audios'
    if AUDIO_PATH.exists() == False or AUDIO_PATH.is_dir() == False:
        q = str(input("Do you want to create folder for audios(Y/n)"))
        if q == "Y":
            AUDIO_PATH.mkdir()
        elif q == "n":
            print("Canceling installation")
            sys.exit(1)
        else:
            print("Something went wrong")
            sys.exit(2)
    with yt_dlp.YoutubeDL(YDL_OTPS) as ydl:
        ydl.download(urls)
    return


if __name__ == "__main__":
    try:
        data = pull_metadata()
        urls = get_urls(data=data)
        download_audios(urls=urls)
    except Exception as e:
        print(f"Something went wrong.\n{e}")
