import requests, threading, youtube_dl
from channels.models import Podcast

API_KEY = 'AIzaSyBh2bOOSuTVIx1At1cksccOWirYtq_jHrA'


def download_mp3_from_video(url, name):
    outtmpl = "static/audio/" + name + '.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', },
            {'key': 'FFmpegMetadata'},
        ],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def search_videos(name, maxRes=50):
    p = {
        'q': name,
        'maxResults': int(maxRes),
        'part': 'snippet',
        'type': 'video',
        'key': API_KEY
    }
    return requests.get("https://www.googleapis.com/youtube/v3/search", params=p).json()


def search_videos_API2(name, maxRes=50):
    found = search_videos(name, maxRes)
    ids = set()
    for i in found['items']:
        ids.add(i['id']['videoId'])
    p = {
        'part': 'snippet,contentDetails,statistics',  # 'snippet,contentDetails,statistics,topicDetails'
        'id': ",".join(ids),
        'key': API_KEY
    }
    return requests.get("https://www.googleapis.com/youtube/v3/videos", params=p).json()


def create_podcast(video_id):
    p = {'part': 'snippet,contentDetails', 'id': video_id, 'key': 'AIzaSyBh2bOOSuTVIx1At1cksccOWirYtq_jHrA'}
    temp = requests.get("https://www.googleapis.com/youtube/v3/videos", params=p).json()
    if len(temp['items']) < 1: return None
    dur = iso_duration_to_seconds(temp['items'][0]['contentDetails']['duration'])
    if dur == 0 or temp['items'][0]['snippet']['liveBroadcastContent'] == "live":
        return None
    obj = Podcast(video_id=video_id)
    obj.name = temp['items'][0]['snippet']['title']
    obj.channel_id = temp['items'][0]['snippet']['channelId']
    obj.channel_name = temp['items'][0]['snippet']['channelTitle']
    obj.thumbnails_url = temp['items'][0]['snippet']['thumbnails']['medium']['url']
    obj.duration = dur
    obj.save()
    return obj


def iso_duration_to_seconds(s):
    s = s[2:]
    times = ['']
    k = 0
    mult = {'S': 1, 'M': 60, 'H': 3600}
    for i in s:
        if i.isdigit():
            times[k] += i
        else:
            times[k] = int(times[k]) * mult[i]
            times.append('')
            k += 1
    times.pop()
    return sum(times)


def download_audio_Thread(video_id, obj):
    t = threading.Thread(target=download_with_hide,
                         args=(video_id, obj))
    t.daemon = True
    t.start()


def download_with_hide(video_id, obj):
    download_mp3_from_video("https://youtu.be/" + video_id, video_id)
    obj.processed = True
    obj.save()
