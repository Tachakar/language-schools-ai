import os
import pprint
import googleapiclient.discovery
def pull_metadata():
    try:
        youtube = googleapiclient.discovery.build(serviceName="youtube", version="v3", developerKey=os.environ.get("google_cloud_api_key"))
        req = youtube.search().list(
            part="snippet",
            maxResults=10,
            videoLicense="creativeCommon",
            q="english lessons",
            type="video",
            videoDuration="medium",
        )
        print("Metadata pulled")
        return req.execute()
    except Exception as e:
        print(f"Something went wrong while pulling metadata, ErrorMessage: {e}")
        return

def get_urls(d: dict):
    videos = d.get('items', None)
    if videos != None:
        urls = []
        for video in videos:
            id = video['id']['videoId']
            url = f"https://www.youtube.com/watch?v={id}"
            urls.append(url)
        print("Got urls")
        return urls
    print("Something went wrong in get_urls()")
    return None

if __name__ == "__main__":
    data = pull_metadata()
    if data != None:
        urls = get_urls(data)
    else:
        urls = None
