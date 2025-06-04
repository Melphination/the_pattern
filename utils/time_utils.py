from datetime import datetime
from typing import List


def parse_time(time_str: str):
    """시간 문자열을 파싱하여 datetime 객체를 반환"""
    return datetime.strptime(time_str, "%H:%M:%S")


def parse_time_range(time_str: str):
    """시간 구간 문자열을 파싱하여 시작시간과 종료시간을 반환"""
    start_str, end_str = time_str.split("-")
    start_time = parse_time(start_str)
    end_time = parse_time(end_str)
    return start_time, end_time


def to_sec(t) -> int:
    """초 단위로 변환"""
    return t.hour * 3600 + t.minute * 60 + t.second


def to_time(seconds: int) -> str:
    """초를 HH:MM:SS 형식 문자열로 변환"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def find_overlap(range1: str, range2: str):
    """두 시간 구간의 겹치는 부분을 찾기"""
    start1, end1 = parse_time_range(range1)
    start2, end2 = parse_time_range(range2)

    # 시간을 초 단위로 변환
    start1_sec = to_sec(start1)
    end1_sec = to_sec(end1)
    start2_sec = to_sec(start2)
    end2_sec = to_sec(end2)

    # 겹치는 구간 계산
    overlap_start = max(start1_sec, start2_sec)
    overlap_end = min(end1_sec, end2_sec)

    # 겹치는 구간이 있는지 확인
    if overlap_start < overlap_end:
        return overlap_start, overlap_end
    else:
        return None


def find_all_overlaps(list1: List[str], list2: List[str]):
    """두 리스트 간의 모든 겹치는 시간 구간을 찾기"""
    overlaps = []

    for range1 in list1:
        for range2 in list2:
            overlap = find_overlap(range1, range2)
            if overlap:
                overlaps.append(overlap)

    return overlaps


def merge_overlapping_intervals(intervals):
    """겹치는 구간들을 병합"""
    if not intervals:
        return []

    # 구간을 시작 시간 기준으로 정렬
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    merged = []
    current_start, current_end = sorted_intervals[0]

    for start, end in sorted_intervals[1:]:
        if start <= current_end:  # 겹치는 경우
            current_end = max(current_end, end)
        else:  # 겹치지 않는 경우
            merged.append(f"{to_time(current_start)}-{to_time(current_end)}")
            current_start, current_end = start, end

    merged.append(f"{to_time(current_start)}-{to_time(current_end)}")
    return merged


def calculate_overlaps(interval1: List[str], interval2: List[str]):
    """두 시간 구간 간의 겹치는 시간을 시간 단위로 계산"""
    intervals = merge_overlapping_intervals(find_all_overlaps(interval1, interval2))
    overlap_time = 0
    for interval in intervals:
        start, end = parse_time_range(interval)
        start_time = to_sec(start)
        end_time = to_sec(end)
        overlap_time += end_time - start_time
    return overlap_time / 3600
