from random import sample, shuffle, randint
from datetime import date, timedelta
from itertools import permutations


def get_random_video_ids(video_ids, length=1):
    video_ids = sample(video_ids, length)
    shuffle(video_ids)

    return video_ids


def quiz_channel_name(channel_info):
    quiz = {
        'type': 'short',
        'quiz': {
            'txt': '이 채널의 이름은 무엇인가요? (@영어 형식으로 작성)',
            'correct_answer': channel_info['snippet']['customUrl']
        }
    }

    return quiz


def quiz_subscriber_count(channel_info):
    subscriber_count = int(channel_info['statistics']['subscriberCount'])
    answers = sample(range(int(subscriber_count * 0.8),
                     int(subscriber_count * 1.2)), 4)
    answers.sort()

    gap = subscriber_count
    correct_answer = 0
    for idx, answer in enumerate(answers):
        temp = abs(subscriber_count - answer)
        if temp < gap:
            correct_answer = idx
            gap = temp

    quiz = {
        'type': 'choice',
        'quiz': {
            'txt': '이 채널의 구독자 수에 가장 가까운 값은 몇 번일까요?',
            'answers': answers,
            'correct_answer': correct_answer
        }
    }

    return quiz


def quiz_video_count(channel_info):
    video_count = int(channel_info['statistics']['videoCount'])
    sample_range = sample(range(int(video_count * 0.8), video_count), 3) + \
        sample(range(video_count + 1, int(video_count * 1.2)), 3)
    answers = [*sample(sample_range, 3), video_count]
    answers.sort()
    correct_answer = answers.index(video_count)

    quiz = {
        'type': 'choice',
        'quiz': {
            'txt': '이 채널에 등록된 총 영상 개수는 몇 개일까요? (SHORTS 포함)',
            'answers': answers,
            'correct_answer': correct_answer
        }
    }

    return quiz


def quiz_channel_view_count(channel_info):
    view_count = int(channel_info['statistics']['viewCount'])
    sample_range = sample(range(int(view_count * 0.8), view_count), 3) + \
        sample(range(view_count + 1, int(view_count * 1.2)), 3)
    answers = [*sample(sample_range, 3), view_count]
    answers.sort()
    correct_answer = answers.index(view_count)

    quiz = {
        'type': 'choice',
        'quiz': {
            'txt': '이 채널의 모든 영상의 조회수를 합한 값은 얼마일까요?',
            'answers': answers,
            'correct_answer': correct_answer
        }
    }

    return quiz


def quiz_video_name(video_infos):
    video_num = randint(0, 3)
    image_url = video_infos[video_num]['thumbnail']
    answers = list(map(lambda x: x['title'], video_infos))
    correct_answer = video_num

    quiz = {
        'type': 'choice',
        'quiz': {
            'txt': '아래 썸네일의 유튜브 제목은 무엇일까요?',
            'items': [
                {
                    'image_url': image_url
                }
            ],
            'answers': answers,
            'correct_answer': correct_answer
        }
    }

    return quiz


def quiz_video_view_count(video_info):
    view_count = video_info['view_count']
    title = video_info['title']
    image_url = video_info['thumbnail']

    sample_range = sample(range(int(view_count * 0.8), view_count), 3) + \
        sample(range(view_count + 1, int(view_count * 1.2)), 3)
    answers = [*sample(sample_range, 3), view_count]
    answers.sort()
    correct_answer = answers.index(view_count)

    quiz = {
        'type': 'choice',
        'quiz': {
            'txt': '이 영상의 조회수는 얼마일까요?',
            'items': [
                {
                    'title': title,
                    'image_url': image_url
                }
            ],
            'answers': answers,
            'correct_answer': correct_answer
        }
    }

    return quiz


def quiz_video_date(video_info):
    title = video_info['snippet']['title']
    image_url = video_info['snippet']['thumbnails']['high']['url']
    publish_date = date.fromisoformat(
        video_info['snippet']['publishedAt'].split('T')[0])

    answers = []
    sample_int = sample(sample(range(-30, 0), 3) + sample(range(1, 30), 3), 3)
    for value in sample_int:
        answer = publish_date + timedelta(days=value)

        answers.append(answer)

    answers.append(publish_date)
    answers.sort()
    correct_answer = answers.index(publish_date)

    quiz = {
        'type': 'choice',
        'quiz': {
            'txt': '이 영상의 업로드일은 언제일까요?',
            'items': [
                {
                    'title': title,
                    'image_url': image_url
                }
            ],
            'answers': answers,
            'correct_answer': correct_answer
        }
    }

    return quiz


def quiz_video_view_count_compare(video_infos):
    items = [{
        'title': item['title'],
        'image_url': item['thumbnail'],
        'view_count': item['view_count']
    } for item in video_infos]

    answers = sample(list(permutations([0, 1, 2], 3)), 4)
    shuffle(answers)
    answer = tuple(sorted([0, 1, 2], key=lambda x: items[x]['view_count']))
    if answer in answers:
        correct_answer = answers.index(answer)
    else:
        correct_answer = randint(0, 3)
        answers[correct_answer] = answer

    quiz = {
        'type': 'choice',
        'quiz': {
            'txt': '영상 조회수가 적은 순서대로 배열된 번호는 몇 번일까요?',
            'items': items,
            'answers': answers,
            'correct_answer': correct_answer
        }
    }

    return quiz


def quiz_video_date_compare(video_infos):
    items = [{
        'title': item['snippet']['title'],
        'image_url': item['snippet']['thumbnails']['high']['url'],
        'publish_date': item['snippet']['publishedAt'].split('T')[0]
    } for item in video_infos]

    answers = sample(list(permutations([0, 1, 2], 3)), 4)
    shuffle(answers)
    answer = tuple(sorted([0, 1, 2], key=lambda x: items[x]['publish_date']))
    if answer in answers:
        correct_answer = answers.index(answer)
    else:
        correct_answer = randint(0, 3)
        answers[correct_answer] = answer

    quiz = {
        'type': 'choice',
        'quiz': {
            'txt': '영상이 오래된 순서대로 배열된 번호는 몇 번일까요?',
            'items': items,
            'answers': answers,
            'correct_answer': correct_answer
        }
    }

    return quiz


def quiz_video_thumbnail(video_infos):
    video_num = randint(0, 3)
    image_url = video_infos[video_num]['title']
    answers = list(map(lambda x: x['thumbnail'], video_infos))
    correct_answer = video_num

    quiz = {
        'type': 'choice',
        'quiz': {
            'txt': '아래 유튜브 제목에 맞는 썸네일은 무엇일까요?',
            'items': [
                {
                    'image_url': image_url
                }
            ],
            'answers': answers,
            'correct_answer': correct_answer
        }
    }

    return quiz


def get_10_quizzes(channel_info, video_infos_short, video_infos_long):
    quizzes = []
    quizzes.append(quiz_channel_name(channel_info))
    quizzes.append(quiz_subscriber_count(channel_info))
    quizzes.append(quiz_video_count(channel_info))
    quizzes.append(quiz_channel_view_count(channel_info))
    quizzes.append(quiz_video_name(video_infos_short[:4]))
    quizzes.append(quiz_video_view_count(video_infos_short[4]))
    quizzes.append(quiz_video_date(video_infos_long[0]))
    quizzes.append(quiz_video_view_count_compare(video_infos_short[5:8]))
    quizzes.append(quiz_video_date_compare(video_infos_long[1:]))
    quizzes.append(quiz_video_thumbnail(video_infos_short[8:]))

    return quizzes


if __name__ == '__main__':
    import test_data

    quizzes = get_10_quizzes(
        test_data.CHANNEL_INFO, test_data.VIDEO_INFOS_SHORT, test_data.VIDEO_INFOS_LONG)

    print(quizzes)
