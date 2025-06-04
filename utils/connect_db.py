import os, sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MongoDB 접속 URI 구성 - 비밀번호 치환
uri = os.environ["MONGO_URI"].replace("<db_password>", os.environ["MONGO_PW"])

# MongoClient 생성 및 서버 API 버전 지정 (v1 사용)
client = MongoClient(uri, server_api=ServerApi("1"))

# MongoDB 서버와의 연결 확인
try:
    client.admin.command("ping")
    print("데이터베이스에 정상적으로 연결되었습니다.")

    users = client["SSHS-Matcher"]["User"]
    rooms = client["SSHS-Matcher"]["Room"]
except Exception as e:
    print(e)
    sys.exit()
