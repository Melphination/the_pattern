import argon2
from utils.connect_db import users


ph = argon2.PasswordHasher()


def create_user(
    email: str, username: str, password: str, gender: str, grade: int, room: int
):
    """새 사용자를 데이터베이스에 등록"""
    email_exists = users.find_one({"email": email})
    username_exists = users.find_one({"username": username})

    if email_exists or username_exists:
        raise ValueError("이메일 또는 아이디가 중복되어 있습니다.")

    user_data = {
        "username": username,
        "email": email,
        "pw": ph.hash(password),
        "patterns": {
            "sleep": ["2025:05:05:23:00:00+A", "2025:05:06:07:00:00-A"],
            "early_bird": [0, 0],
            "light_off": ["2025:05:05:23:00:000"],
            "air": ["2025:05:05:12:00:00+A", "2025:05:05:13:00:00-A"],
            "study": ["2025:05:05:16:00:00+A", "2025:05:05:18:00:00-A"],
        },
        "roommate": [],
        "summary": {
            "sleep": [],
            "early_bird": 0.0,
            "light_off": 0.0,
            "air": [],
            "study": [],
        },
        "gender": gender,
        "grade": grade,
        "room": room,
    }
    users.insert_one(user_data)


def authenticate(username: str, password: str):
    """사용자 인증"""
    user = users.find_one({"username": username})
    if not user:
        return False

    try:
        ph.verify(user["pw"], password)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False
