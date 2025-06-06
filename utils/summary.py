from collections import defaultdict
from utils.time_utils import parse_time, to_sec, to_time
import math
from utils.pattern_types import TIME_PATTERNS, LIKELY_PATTERNS, OFF_PATTERN


def calculate_time_difference(time1: int, time2: int) -> int:
    """
    두 시간 사이의 최소 간격 계산
    자정을 넘나드는 시간 간격도 고려 (예: 23:00과 01:00 사이는 2시간)
    """
    return min(time1 - time2, time1 + 24 * 3600 - time2)

def circular_mean(times):
    """ Circular Mean 계산 """
    angles = [2 * math.pi * (t / (24 * 3600)) for t in times]
    x_vals = [math.cos(a) for a in angles]
    y_vals = [math.sin(a) for a in angles]
    
    avg_x = sum(x_vals) / len(x_vals)
    avg_y = sum(y_vals) / len(y_vals)
    
    avg_angle = math.atan2(avg_y, avg_x)
    if avg_angle < 0:
        avg_angle += 2 * math.pi

    return (avg_angle / (2 * math.pi)) * 24 * 3600

def group_similar_times(times, max_difference_minutes=45):
    """비슷한 시간들을 그룹화하고 평균값 계산"""
    if not times:
        return []

    times.sort()
    grouped_averages = []
    i = 0

    while i < len(times):
        group = [times[i]]

        # 45분 이내 차이나는 시간들을 그룹에 추가
        j = i + 1
        while j < len(times):
            if (
                calculate_time_difference(times[j], times[i])
                <= max_difference_minutes * 60
            ):
                group.append(times[j])
            else:
                break
            j += 1

        # 그룹의 평균값 계산 (circular mean)
        average_time = circular_mean(group)
        grouped_averages.append([average_time, len(group)])

        i = max(j, i + 1)

    return grouped_averages


def organize(patterns):
    """패턴 데이터를 분석하여 일부 정리"""
    organized = defaultdict(list)

    for pattern_name, pattern_data in patterns.items():
        if pattern_name in TIME_PATTERNS:
            # 시간 패턴 처리 (마지막 문자로 +/- 구분)
            for entry in pattern_data:
                time_seconds = to_sec(parse_time(entry[-10:-2]))
                sign = entry[-2]  # '+' 또는 '-'
                organized[f"{pattern_name}{sign}"].append(time_seconds)

        elif pattern_name == OFF_PATTERN:
            organized[pattern_name] = pattern_data

        elif pattern_name == LIKELY_PATTERNS:
            # [얼리버드 횟수, 기록 횟수] 형태로 저장
            organized[pattern_name] = [pattern_data.count("1"), len(pattern_data)]

    return organized


def calculate_statistics(times):
    """패턴 데이터로부터 통계 계산"""
    result = {
        "sleep": [],
        "early_bird": 0.0,
        "light_off": 0.0,
        "air": [],
        "study": [],
    }

    grouped_patterns = defaultdict(list)

    for key, time_list in times.items():
        if key.endswith(("+", "-")):
            # 시간 그룹화 및 평균 계산
            grouped_patterns[key] = group_similar_times(time_list)

        elif key == "early_bird":
            # 조기 기상 비율 계산
            total_sum, count = time_list
            result[key] = total_sum / max(1, count)

        elif key == "light_off":
            # 조명 끄기 비율 계산 (마지막 문자가 '1'인 항목의 비율)
            on_count = len([entry for entry in time_list if entry[-1] == "1"])
            result[key] = on_count / max(1, len(time_list))

    return result, grouped_patterns


def create_time_ranges(grouped_times):
    """시작 시간(+)과 종료 시간(-)을 매칭하여 시간 범위 생성"""
    time_ranges = defaultdict(list)

    for activity in TIME_PATTERNS:
        start_times = grouped_times.get(f"{activity}+", [])
        end_times = grouped_times.get(f"{activity}-", [])

        for start_time in start_times:
            # 시작 시간보다 늦은 첫 번째 종료 시간 찾기
            matching_end_time = None

            for end_time in end_times:
                if start_time < end_time:
                    matching_end_time = end_time
                    break

            # 매칭되는 종료 시간이 없으면 특별한 경우 처리
            if matching_end_time is None:
                if (
                    start_time == start_times[-1]
                    and end_times
                    and end_times[0] < start_times[0]
                ):
                    matching_end_time = end_times[0]
                else:
                    continue

            # 시간 범위 문자열 생성
            start_str = to_time(round(start_time))
            end_str = to_time(round(matching_end_time))
            time_ranges[activity].append(f"{start_str}-{end_str}")

    return time_ranges


def summarize(data):
    """패턴 데이터를 분석하여 요약 통계 생성"""
    patterns = data["patterns"]

    # 데이터 일부 정리
    organized = organize(patterns)

    # 통계 계산
    result, grouped_times = calculate_statistics(organized)

    # 구한 시간대에서 상위 2개의 시간대만 고려
    for pattern in TIME_PATTERNS:
        for sign in "+-":
            grouped_times[pattern + sign].sort(key=lambda x: x[1])
            grouped_times[pattern + sign] = list(map(lambda x: x[0], grouped_times[pattern][-2:])) # 시간대만 남김

    # 시간 범위 생성
    time_ranges = create_time_ranges(grouped_times)

    # 결과에 시간 범위 추가
    for activity in ["sleep", "air", "study"]:
        result[activity] = time_ranges[activity]

    return result
