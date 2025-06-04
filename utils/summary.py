from collections import defaultdict
from utils.time_utils import parse_time, to_sec, to_time


def calculate_time_difference(time1: int, time2: int) -> int:
    """
    두 시간 사이의 최소 간격 계산
    자정을 넘나드는 시간 간격도 고려 (예: 23:00과 01:00 사이는 2시간)
    """
    return min(time1 - time2, time1 + 24 * 3600 - time2)


def group_similar_times(times, max_difference_minutes=45):
    """비슷한 시간들을 그룹화하고 평균값 계산"""
    if not times:
        return []

    times.sort()
    grouped_averages = []
    i = 0

    while i < len(times):
        group = [times[i]]

        # 현재 시간과 45분 이내 차이나는 시간들을 그룹에 추가
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

        # 그룹의 평균값 계산
        average_time = round(sum(group) / len(group))
        grouped_averages.append(average_time)

        i = max(j, i + 1)

    return grouped_averages


def extract_time_data(patterns):
    """패턴 데이터에서 시간 정보 추출"""
    times = defaultdict(list)

    for pattern_name, pattern_data in patterns.items():
        if pattern_name in ["sleep", "air", "study"]:
            # 시간 패턴 처리 (마지막 문자로 +/- 구분)
            for entry in pattern_data:
                time_seconds = to_sec(parse_time(entry[-10:-2]))
                sign = entry[-2]  # '+' 또는 '-'
                times[f"{pattern_name}{sign}"].append(time_seconds)

        elif pattern_name == "light_off":
            times[pattern_name] = pattern_data

        elif pattern_name == "early_bird":
            # [합계, 개수] 형태로 저장
            times[pattern_name] = [sum(pattern_data), len(pattern_data)]

    return times


def calculate_statistics(times):
    """시간 데이터로부터 통계 계산"""
    result = {
        "sleep": [],
        "early_bird": 0.0,
        "light_off": 0.0,
        "air": [],
        "study": [],
    }

    grouped_times = defaultdict(list)

    for key, time_list in times.items():
        if key.endswith(("+", "-")):
            # 시간 그룹화 및 평균 계산
            grouped_times[key] = group_similar_times(time_list)

        elif key == "early_bird":
            # 조기 기상 비율 계산
            total_sum, count = time_list
            result[key] = total_sum / max(1, count)

        elif key == "light_off":
            # 조명 끄기 비율 계산 (마지막 문자가 '1'인 항목의 비율)
            on_count = len([entry for entry in time_list if entry[-1] == "1"])
            result[key] = on_count / max(1, len(time_list))

    return result, grouped_times


def create_time_ranges(grouped_times):
    """시작 시간(+)과 종료 시간(-)을 매칭하여 시간 범위 생성"""
    time_ranges = defaultdict(list)

    for activity in ["sleep", "air", "study"]:
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
    # 데이터 형식 통일
    patterns = data["patterns"]

    # 시간 데이터 추출
    times = extract_time_data(patterns)

    # 통계 계산
    result, grouped_times = calculate_statistics(times)

    # 시간 범위 생성
    time_ranges = create_time_ranges(grouped_times)

    # 결과에 시간 범위 추가
    for activity in ["sleep", "air", "study"]:
        result[activity] = time_ranges[activity]

    return result
