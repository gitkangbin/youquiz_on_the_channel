import re
import json
import requests


def get_video_info_from_request(custom_url):
    url = 'https://youtube.com/{}/videos'.format(custom_url)

    html = ''
    with requests.get(url) as resp:
        if resp.status_code == 200:
            html = resp.text

    pattern = re.compile(r'var ytInitialData = (.*?);')
    fields = pattern.findall(html)
    json_data = []
    if len(fields) > 0:
        json_data = json.loads(fields[0])
        contents = json_data['contents']['twoColumnBrowseResultsRenderer'][
            'tabs'][1]['tabRenderer']['content']['richGridRenderer']['contents']

    videos = {}
    for content in contents[:-1]:
        video_renderer = content['richItemRenderer']['content']['videoRenderer']
        video_id = video_renderer['videoId']
        video = {
            'id': video_id,
            'thumbnail': video_renderer['thumbnail']['thumbnails'][-1]['url'].split('?')[0],
            'title': video_renderer['title']['runs'][-1]['text'],
            'description': video_renderer['descriptionSnippet']['runs'][-1]['text'],
            'time_text': video_renderer['lengthText']['simpleText'],
            'view_count': int(re.sub('[^0-9]', '', video_renderer['viewCountText']['simpleText'])),
        }

        videos[video_id] = video

    return videos


if __name__ == "__main__":
    custom_url = '@dlwlrma'
    video_infos = get_video_info_from_request(custom_url)

    print('Get last 30 video names in channel name: {}'.format(custom_url))
    for idx, key in enumerate(video_infos):
        print(idx + 1, video_infos[key]['title'], key)
