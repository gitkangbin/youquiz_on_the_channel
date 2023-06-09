# YouTube 채널 퀴즈

## 사용 환경 구축

### Virtualenv 설정
아래 명령어를 순차적으로 실행하여 Python 가상 환경을 만들고 필요한 라이브러리를 다운로드 한다.
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv)$ pip install -r requirements.txt
```

### settings 설정
아래 명령어를 실행하여 settings_local.py 파일을 생성한다. settings_local.py는 settings.py에서 참조한다.
```sh
$ cp settings_local.py.example settings_local.py
```

### Youtube Data API Key 획득
https://console.cloud.google.com/apis/dashboard 에서 Youtube Data API v3의 key를 발급 받아 settings_local.py 파일의 KEY에 값을 입력한다.

## 실행 테스트

### youtube_api
YouTube API를 활용해서 채널과 영상 정보를 가져올 수 있다. 아래 명령어를 사용해 테스트를 할 수 있다.
```sh
(.venv)$ python youtue_api.py
```

### youtube_requests
requests를 사용해 특정 채널의 영상 정보를 가져올 수 있다. 아래 명령어를 사용해 테스트를 할 수 있다.
```sh
(.venv)$ python youtue_requests.py
```

### quiz
데이터에 맞는 퀴즈를 생성해 반환한다. 아래 명령어를 사용해 테스트를 할 수 있다. 테스트 시에는 test_data.py의 정보를 사용해 테스트를 한다.
```sh
(.venv)$ python quiz.py
```

### test
youtube_api, youtube_requests, quiz 파일이 실행되는 일련의 과정을 테스트할 수 있다. 아래 명령어를 사용해 테스트를 할 수 있다.
```sh
(.venv)$ python test.py
```