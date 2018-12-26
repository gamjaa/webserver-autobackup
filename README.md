# webserver-autobackup

`backup_files` 폴더 내의 파일을 구글 드라이브에 업로드합니다.

## 사용법

1. [Google Cloud Platform](https://console.cloud.google.com/)에서 프로젝트 생성 후 Google Drive API 사용

   1. 사용자 인증 정보(OAuth 클라이언트 ID -> 기타) 생성
   2. JSON 파일 다운 받아서 `client_secrets.json`로 파일 이름 변경

2. `config.ini` 파일 작성

   ```
   [DEFAULT]
   PARENT_FOLDER_ID = (날짜별 백업 폴더를 생성할 폴더 ID)
   ```

   - 폴더 ID는 Google Drive 내 URL로 확인할 수 있습니다.

     `https://drive.google.com/drive/folders/(폴더 ID)`

3. PyDrive 설치

   `pip3 install PyDrive`

4. `run.py` 실행

   `python3 run.py`

   - 실행 시 최초 1회 인증 과정을 진행합니다. 출력된 URL에 접속해 발급 받은 코드를 입력해주세요.
     - `auth_only.py` 실행 시에 해당 인증 과정만 진행 후 종료됩니다.
     - 인증 과정이 끝나면 `credentials.json` 파일이 생성됩니다.
   - `YYYY-mm-dd` 형식의 폴더를 생성해 `backup_files` 폴더 내 파일을 업로드합니다.

## 추가 설명

아래와 같은 sh 파일을 작성해서 `crontab`으로 주기적으로 자동 실행되도록 사용하고 있습니다.

```
#! /bin/bash
cd /home/(USERNAME)/webserver-autobackup

mysqldump -u (USERNAME) -p'(PASSWORD)' (DBNAME) > ./backup_files/db.sql

tar -cf ./backup_files/(FILENAME).tar (ANY_FOLDER)

python3 run.py
```

