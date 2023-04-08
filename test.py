from quiz import get_random_video_ids, get_10_quizzes
from youtube_requests import get_video_info_from_request
from youtube_api import get_youtube, get_channels, select_channel, get_channel_info, get_video_infos_from_video_api

from oauth2client.tools import argparser


def main(q):
    youtube = get_youtube()

    channels = get_channels(youtube, q)
    channel = select_channel(channels)
    channel_info = get_channel_info(youtube, channel['channelId'])['items'][0]

    video_infos_from_request = get_video_info_from_request(
        channel_info['snippet']['customUrl'])
    video_ids = get_random_video_ids(video_infos_from_request.keys(), 16)
    video_infos_short = [values for key,
                         values in video_infos_from_request.items() if key in video_ids[:12]]
    video_infos_long = get_video_infos_from_video_api(
        youtube, video_ids[12:])
    
    quizzes = get_10_quizzes(channel_info, video_infos_short, video_infos_long)
    print(quizzes)


if __name__ == "__main__":
    argparser.add_argument("-q", help="Search term", default="Google")
    args = argparser.parse_args()

    main(args.q)
