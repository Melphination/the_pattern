from matcher.utils.user_utils import User
from utils.pattern_types import TIME_PATTERNS, LIKELY_PATTERNS, OFF_PATTERN
from utils.time_utils import calculate_overlaps

PATTERN_WEIGHTS = {
    "sleep": 3,
    "early_bird": 2,
    "air": 1,
    "light_off": 2.7,
    "study": 3,
}


def calculate_score(user1: User, user2: User) -> float:
    """두 사용자 간 선호도 점수 계산"""
    total_score = 0
    for pattern, weight in PATTERN_WEIGHTS.items():
        pattern_score = calculate_pattern_difference(user1, user2, pattern)
        total_score += pattern_score * weight
    return total_score


def calculate_triplet_score(user1: User, user2: User, user3: User) -> float:
    """3인 조합의 평균 선호도 점수 계산"""
    score1 = calculate_score(user1, user2)
    score2 = calculate_score(user2, user3)
    score3 = calculate_score(user3, user1)
    return (score1 + score2 + score3) / 3


def passes_filtering(user1: User, user2: User) -> bool:
    """매칭 필터링 통과 여부"""
    if not user1.is_compatible_with(user2):
        return False

    # 수면 시간과 소등 시간 기반 추가 필터링
    sleep_diff = calculate_pattern_difference(user1, user2, "sleep")
    light_score = calculate_pattern_difference(user1, user2, "light_off")

    sleep_compatible = sleep_diff <= 1 or (sleep_diff <= 2 and light_score >= 0.5)
    return sleep_compatible


def calculate_pattern_difference(user1: User, user2: User, pattern: str) -> float:
    """특정 패턴에 대한 두 사용자 간 차이 계산"""
    pattern1 = user1.summary[pattern]
    pattern2 = user2.summary[pattern]

    if pattern in TIME_PATTERNS:
        return calculate_overlaps(pattern1, pattern2)
    elif pattern == OFF_PATTERN:
        return (pattern1 + pattern2) / 2
    elif pattern in LIKELY_PATTERNS:
        return abs(pattern1 - pattern2)

    return 0.0
