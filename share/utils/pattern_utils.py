import re
from utils.summary import summarize
from utils.connect_db import users
from datetime import datetime


def validate_date_format(date):
    try:
        datetime.strptime(date, "%Y:%m:%d:%H:%M:%S")
    except:
        return False
    else:
        return True


def validate_pattern_format(name, patterns):
    """패턴 형식 유효성 검사"""
    for pattern in patterns.split(" "):
        if name in ["sleep", "air", "study"] and not (
            re.fullmatch(r"[+-][PA]", pattern[-2:])
            and validate_date_format(pattern[:-2])
        ):
            return False
        elif name == "light_off" and not (
            pattern[-1] in "01" and validate_date_format(pattern[:-1])
        ):
            return False
    if name == "early_bird":
        return bool(re.fullmatch(r"[01]*", patterns))

    return True


def stringify_pattern(pattern):
    """패턴을 문자열로 변환"""
    pattern_type = type(pattern)
    if pattern_type is list:
        return " ".join(map(str, pattern))
    elif pattern_type in (float, int):
        return str(pattern)
    elif pattern_type is str:
        return pattern
    raise "포맷이 맞지 않습니다."


def save_patterns(username, sheet_data):
    """패턴 데이터 저장"""
    user = users.find_one({"username": username})
    if not user:
        return False, "사용자를 찾을 수 없습니다."

    patterns = user["patterns"]

    i = 2
    while sheet_data.get(f"A{i}", "") != "":
        try:
            name, pattern = sheet_data[f"A{i}"].split(" ", 1)
            if len(pattern) != 0 and not validate_pattern_format(name, pattern):
                return False, f"A{i}에서 포맷이 맞지 않습니다."

            if name == "early_bird":
                patterns[name] = pattern
            else:
                patterns[name].append(pattern)

        except:
            return False, f"A{i}에서 포맷이 맞지 않습니다."

        i += 1

    # 중복 제거
    for key, value in patterns.items():
        if key != "early_bird":
            patterns[key] = list(set(value))

    users.update_one({"username": username}, {"$set": {"patterns": patterns}})
    return True, ""


def get_user_patterns_display(username):
    """사용자 패턴을 표시용으로 포맷"""
    user = users.find_one({"username": username})
    if not user:
        return []

    data = [[username]]
    for name, pattern in user["patterns"].items():
        data.append([f"{name} {stringify_pattern(pattern)}"])

    return data


def get_roommate_patterns_display(username):
    """룸메이트 패턴을 표시용으로 포맷"""
    user = users.find_one({"username": username})
    if not user:
        return [], []

    roommates = user["roommate"]

    # 룸메이트 요약 정보 업데이트
    for roommate in roommates:
        email = f"{roommate}@sshs.hs.kr"
        roommate_user = users.find_one({"email": email})
        if roommate_user:
            summary = summarize(roommate_user)
            users.update_one({"email": email}, {"$set": {"summary": summary}})

    # 룸메이트 패턴 데이터 구성
    roommate_patterns = []
    for roommate in roommates:
        email = f"{roommate}@sshs.hs.kr"
        roommate_user = users.find_one({"email": email})
        if roommate_user:
            patterns = [
                f"{name} {stringify_pattern(pattern)}"
                for name, pattern in roommate_user["summary"].items()
            ]
            roommate_patterns.append(patterns)

    if roommate_patterns:
        roommate_patterns = list(zip(*roommate_patterns))

    return roommates, list(roommate_patterns)
