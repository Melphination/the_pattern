def get_category(user) -> int:
    """사용자의 성별과 학년에 따라 고유 숫자를 반환"""
    gender_offset = 3 if user["gender"] == "F" else 0
    grade_offset = user["grade"] - 1
    return gender_offset + grade_offset


def is_compatible_with(user1, user2) -> bool:
    """기본적인 매칭 조건 검사 (성별과 학년이 같아야 함)"""
    return user1["gender"] == user2["gender"] and user1["grade"] == user2["grade"]
