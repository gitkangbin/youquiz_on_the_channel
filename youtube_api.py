from settings import API_SERVICE_NAME, API_VERSION, KEY, MAX__VIDEO_RESULTS

from apiclient.discovery import build
from apiclient.errors import HttpError


def get_youtube():
    # Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
    # tab of
    #   https://cloud.google.com/console
    # Please ensure that you have enabled the YouTube Data API for your project.
    try:
        youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=KEY)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        exit()

    return youtube


def get_channels(youtube, q):
    try:
        # https://developers.google.com/youtube/v3/docs/search?hl=ko
        resp = youtube.search().list(part='snippet', q=q, type='channel').execute()
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        exit()

    channels = []
    for item in resp.get('items', []):
        channel = {}
        snippet = item['snippet']

        channel['title'] = snippet['title']
        channel['desc'] = snippet['description']
        channel['thumbnail'] = snippet['thumbnails']['default']['url']
        channel['channelId'] = snippet['channelId']

        channels.append(channel)

    return channels


def show_channels(channels):
    for idx, channel in enumerate(channels):
        print('{}: {} - {}'.format(idx + 1, channel['title'], channel['desc']))


def select_channel(channels):
    show_channels(channels)
    num = input('선택하고 싶은 채널의 번호를 입력해주세요(1 ~ {}): '.format(len(channels)))

    return channels[int(num) - 1]


def get_channel_info(youtube, channel_id):
    try:
        # https://developers.google.com/youtube/v3/docs/channels?hl=ko
        channel_info = youtube.channels().list(
            part='snippet,statistics', id=channel_id, maxResults=1).execute()
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        exit()

    return channel_info


def get_video_ids_from_search_api(youtube, channel_id, repeat_count=1):
    result = []
    try:
        # https://developers.google.com/youtube/v3/docs/search?hl=ko
        page_token = ''
        for _ in range(repeat_count):
            resp = youtube.search().list(part='id', channelId=channel_id, maxResults=MAX__VIDEO_RESULTS,
                                         order='date', pageToken=page_token, type='video', videoDuration='medium').execute()
            page_token = resp['nextPageToken']
            result += resp['items']
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        exit()

    return result


def get_video_infos_from_video_api(youtube, video_ids):
    video_id_string = ','.join(video_ids)

    try:
        # https://developers.google.com/youtube/v3/docs/videos?hl=ko
        resp = youtube.videos().list(part='snippet,statistics', id=video_id_string).execute()
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        exit()

    return resp.get('items', [])


if __name__ == '__main__':
    q = '아이유'
    youtube = get_youtube()
    channels = get_channels(youtube, q)
    print('Get 5 channels related to query: {}'.format(q))
    show_channels(channels)

    # https://www.youtube.com/channel/UC3SyT4_WLHzN7JmHQwKQZww
    channel_id = 'UC3SyT4_WLHzN7JmHQwKQZww'
    video_ids = get_video_ids_from_search_api(youtube, channel_id)
    video_infos = get_video_infos_from_video_api(youtube, video_ids)

    print('\nGet last 5 video names in channelID: {}'.format(channel_id))
    for idx, item in enumerate(video_infos):
        print(idx + 1, item['snippet']['title'])
