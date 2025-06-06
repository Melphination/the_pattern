import argon2
from utils.connect_db import users


ph = argon2.PasswordHasher()


def create_user(
    email: str, username: str, password: str, gender: str, grade: int, room: int
):
    """새 사용자를 데이터베이스에 등록"""
    user_data = {
        "username": username,
        "email": email,
        "pw": ph.hash(password),
        "patterns": {
            "sleep": ["2025:05:05:23:00:00+A", "2025:05:06:07:00:00-A"],
            "early_bird": "",
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
        "exclude": False,
        "bonus": 0,
        "minus": 0,
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
