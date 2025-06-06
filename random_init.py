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
emails = ["25039@sshs.hs.kr", "26000@sshs.hs.kr"]

users.insert_one(
    {
        "gender": "M",
        "grade": 1,
        "username": "Admin",
        "pw": os.environ["ADMIN_PW"],
        "email": "26000@sshs.hs.kr",
        "summary": {
            "sleep": [],
            "early_bird": 0.0,
            "light_off": 0.0,
            "air": [],
            "study": [],
        },
        "patterns": {
            "sleep": [],
            "early_bird": "",
            "light_off": [],
            "air": [],
            "study": [],
        },
        "roommate": [],
        "room": 500,
        "exclude": True,
        "bonus": 0,
        "minus": 0,
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
        email = f"{random.randint(23001, 25999)}@sshs.hs.kr"
    emails.append(email)

# 150명의 무작위 사용자 삽입
random_users = []
for username, email in zip(usernames[2:], emails[2:]):
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
                "early_bird": "",
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
            "exclude": False,
            "bonus": random.randint(0, 10),
            "minus": random.randint(0, 10),
        }
    )

users.insert_many(random_users)

# 방 정보 삽입
rooms.insert_many(
    [
        {
            "number": i,
            "students": tuple(),
            "floor": i // 100,
            "reset": False,
            "category": [0],
        }
        for i in list(range(501, 519)) +list(range(520, 539))
    ]
)

rooms.insert_many(
    [
        {
            "number": i,
            "students": tuple(),
            "floor": i // 100,
            "reset": False,
            "category": [1, 2],
        }
        for i in list(range(403, 419)) + list(range(420, 439)) + list(range(301, 312)) + list(range(313, 324))
    ]
)

rooms.insert_many(
    [
        {
            "number": i,
            "students": tuple(),
            "floor": i // 100,
            "reset": False,
            "category": [0, 1, 2],
        }
        for i in range(401, 403)
    ]
)

rooms.insert_many(
    [
        {
            "number": i,
            "students": tuple(),
            "floor": i // 100,
            "reset": False,
            "category": [3, 4, 5],
        }
        for i in range(201, 223)
    ]
)

rooms.insert_many(
    [
        {
            "number": i,
            "students": tuple(),
            "floor": i // 100,
            "reset": False,
            "category": [6],
        }
        for i in list(range(361, 372)) + list(range(451, 476))
    ]
)
