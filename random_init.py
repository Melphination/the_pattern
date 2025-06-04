from utils.connect_db import rooms, users
import random, argon2
import string
import os, dotenv

dotenv.load_dotenv()

# 모든 유저와 방 데이터를 초기화 (기존 데이터 삭제)
users.delete_many({})
rooms.delete_many({})

ph = argon2.PasswordHasher()

# 가능한 성별과 학년 리스트 정의
genders = ["M", "F"]
grades = [1, 2, 3]

usernames = ["Penguin", "Admin"]
emails = ["25039@sshs.hs.kr", "25999@sshs.hs.kr"]

users.insert_one(
    {
        "gender": "M",
        "grade": 1,
        "username": "Admin",
        "pw": os.environ["ADMIN_PW"],
        "email": "25999@sshs.hs.kr",
        "summary": {
            "sleep": [],
            "early_bird": 0.0,
            "light_off": 0.0,
            "air": [],
            "study": [],
        },
        "patterns": {
            "sleep": [],
            "early_bird": [0, 0],
            "light_off": [],
            "air": [],
            "study": [],
        },
        "roommate": [],
        "room": 500,
    }
)

pw = os.environ["ADMIN_PW"]

for _ in range(150):
    username = "Penguin"
    while username in usernames:
        username = "".join(
            random.choices(string.ascii_letters + "_", k=random.randint(8, 12))
        )
    usernames.append(username)
    email = "25039@sshs.hs.kr"
    while email in emails:
        email = f"{random.randint(23000, 25999)}@sshs.hs.kr"
    emails.append(email)

# 150명의 무작위 사용자 삽입
random_users = []
for username, email in zip(usernames[1:], emails[1:]):
    random_users.append(
        {
            "gender": random.choice(genders),
            "grade": random.choice(grades),
            "username": username,
            "pw": pw,
            "summary": {
                "sleep": [],
                "early_bird": 0.0,
                "light_off": 0.0,
                "air": [],
                "study": [],
            },
            "patterns": {
                "sleep": [
                    f"2025:05:05:{random.randint(20, 25) % 24:02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}+P",
                    f"2025:05:05:{random.randint(6, 7):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}-P",
                ],
                "early_bird": [1, 0, 1],
                "light_off": [
                    f"2025:05:05:{random.randint(14, 15):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}1"
                ],
                "air": [
                    f"2025:05:05:{random.randint(12, 13):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}+P",
                    f"2025:05:05:{random.randint(14, 15):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}-P",
                ],
                "study": [
                    f"2025:05:05:{random.randint(16, 17):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}+P",
                    f"2025:05:05:{random.randint(18, 19):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}-P",
                ],
            },
            "email": email,
            "roommate": [],
            "room": 500,
        }
    )

users.insert_many(random_users)


# 기숙사 방 번호 리스트 생성: 201–298, 301–398, 401–498, 501–598
nums = list(range(201, 299))
nums += list(range(301, 399))
nums += list(range(401, 499))
nums += list(range(501, 599))

# 방 정보 삽입
rooms.insert_many(
    [
        {
            "number": i,
            "students": tuple(),
            "floor": i // 100,
            "place": "old",
            "reset": False,
        }
        for i in nums
    ]
)
