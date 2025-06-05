from collections import defaultdict
from typing import List, Dict, Optional, Any
from random import shuffle, choice
import tkinter as tk

from utils.combine import combine
from utils.connect_db import rooms as rooms_db
from utils.connect_db import users as users_db
from utils.summary import summarize
from matcher.utils.scoring_utils import (
    calculate_score,
    calculate_triplet_score,
    passes_filtering,
)
from matcher.utils.user_utils import get_category


def execute_matching(root: tk.Tk, progress_bar) -> List[Any]:
    """메인 매칭 실행 함수"""
    print("그리디 매칭 시작")

    # 1. 데이터 전처리
    preprocess_data(progress_bar, root)

    # 2. 사용자 데이터 로드 및 셔플
    users_by_category = load_and_shuffle_users()
    progress_bar["value"] = 40
    root.update()

    # 3. 후보 생성
    candidates = generate_candidates(users_by_category)
    progress_bar["value"] = 47
    root.update()

    # 4. 그리디 매칭 수행
    matched_pairs = perform_greedy_matching(candidates, users_by_category)
    progress_bar["value"] = 70
    root.update()

    print("그리디 매칭 완료")
    return matched_pairs


def assign_rooms(matched_pairs: List[Any], progress_bar, root: tk.Tk):
    """매칭된 쌍들을 방에 배정"""
    shuffle(matched_pairs)

    # 층별 사용 가능한 방 조회
    available_rooms = get_available_rooms_by_category()

    for pair in matched_pairs:
        room = select_room_for_pair(pair, available_rooms)
        if room:
            assign_pair_to_room(pair, room)

    progress_bar["value"] = 80
    root.update()

    # 방 상태 정리
    cleanup_rooms()
    progress_bar["value"] = 100


def preprocess_data(progress_bar, root):
    """데이터 전처리"""
    print("중복된 패턴 제거")
    combine()
    progress_bar["value"] = 10
    root.update()

    print("패턴 정리")
    users = users_db.find({"admin": False})
    for user in users:
        summary = summarize(user)
        users_db.update_one({"username": user}, {"$set": {"summary": summary}})

    progress_bar["value"] = 20
    root.update()


def load_and_shuffle_users() -> List[List[Any]]:
    """사용자 데이터를 카테고리별로 로드하고 셔플"""
    users_by_category = [[]] * 7
    users = users_db.find({"admin": False})
    for user in users:
        category = get_category(user)
        users_by_category[category].append(user)
    for i in range(len(users_by_category)):
        shuffle(users_by_category[i])

    return users_by_category


def generate_candidates(users_by_category: List[List[Any]]) -> Dict[float, List[Any]]:
    """매칭 후보들을 생성하고 점수별로 분류"""
    candidates = defaultdict(list)

    for users in users_by_category:
        generate_pairs_for_category(users, candidates)
        generate_triplets_for_category(users, candidates)

    return candidates


def generate_pairs_for_category(users: List[Any], candidates: Dict[float, List[Any]]):
    """2인 조합 생성"""
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            user1, user2 = users[i], users[j]
            if passes_filtering(user1, user2):
                score = calculate_score(user1, user2)
                candidates[score].append([(user1, user2), score])


def generate_triplets_for_category(
    users: List[Any], candidates: Dict[float, List[Any]]
):
    """3인 조합 생성"""
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            for k in range(j + 1, len(users)):
                user1, user2, user3 = users[i], users[j], users[k]
                if (
                    passes_filtering(user1, user2)
                    and passes_filtering(user2, user3)
                    and passes_filtering(user1, user3)
                ):
                    avg_score = calculate_triplet_score(user1, user2, user3)
                    candidates[avg_score].append([(user1, user2, user3), avg_score])


def perform_greedy_matching(
    candidates: Dict[float, List[Any]],
    users_by_category: List[List[Any]],
) -> List[Any]:
    """그리디 알고리즘으로 매칭 수행"""
    matched_pairs = []
    available_users = []
    for users in users_by_category:
        available_users.extend(users)

    # 각 카테고리별 2인 조합 필요 개수 계산
    need_pairs = [calculate_needed_pairs(len(users)) for users in users_by_category]

    # 점수 높은 순으로 매칭
    for score in sorted(candidates.keys(), reverse=True):
        for pair in candidates[score]:
            if can_match_pair(pair, available_users, need_pairs):
                matched_pairs.append(pair)
                update_matching_state(pair, available_users, need_pairs)

    return matched_pairs


def calculate_needed_pairs(total_users: int) -> int:
    """카테고리별 필요한 2인 조합 개수 계산"""
    remainder = total_users % 3
    return 2 if remainder == 1 else (1 if remainder == 2 else 0)


def can_match_pair(
    pair: List[Any], available_users: set, need_pairs: List[int]
) -> bool:
    """매칭 가능 여부 확인"""
    if not all(user in available_users for user in pair[0]):
        return False

    category = get_category(pair[0][0])
    if len(pair[0]) == 2 and need_pairs[category] == 0:
        return False

    return True


def update_matching_state(pair: List[Any], available_users: set, need_pairs: List[int]):
    """매칭 상태 업데이트"""
    if len(pair[0]) == 2:
        need_pairs[get_category(pair[0][0])] -= 1

    for user in pair[0]:
        available_users.remove(user)


def get_available_rooms_by_category() -> Dict[int, List[Any]]:
    """방을 종류별로 분류"""
    rooms = list(rooms_db.aggregate([{"$unwind": "$category"}]))
    rooms_by_category = defaultdict(list)
    for room in rooms:
        rooms_by_category[room["category"]].append(room)
    return rooms_by_category


def select_room_for_pair(
    pair: List[Any], available_rooms: Dict[int, List[Any]]
) -> Optional[Any]:
    """매칭 쌍에 적합한 방 선택"""
    category = get_category(pair[0][0])

    rooms = available_rooms.get(category, [])

    if rooms:
        room = choice(rooms)
        rooms.remove(room)
        return room
    return None


def assign_pair_to_room(pair: List[Any], room):
    """매칭 쌍을 방에 배정"""
    user_data = tuple({"username": user["username"]} for user in pair[0])
    rooms_db.update_one(
        {"number": room["number"]},
        {"$set": {"students": user_data, "reset": True}},
    )

    # 사용자 정보 업데이트
    for user in pair[0]:
        roommates = [
            u["username"] for u in pair[0] if u["username"] != user["username"]
        ]
        users_db.update_one(
            {"username": user["username"]},
            {"$set": {"room": room["number"], "roommate": roommates}},
        )


def cleanup_rooms():
    """방 상태 정리"""
    all_rooms = rooms_db.find()
    for room in all_rooms:
        if not room["reset"]:
            room["students"] = ()
        rooms_db.update_one(
            {"number": room["number"]},
            {"$set": {"students": room["students"], "reset": False}},
        )
