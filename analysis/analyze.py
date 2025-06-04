from analysis.inputs import sensors, SensorType
from utils.pattern_types import TIME_PATTERNS, OFF_PATTERN
from utils.connect_db import users
from datetime import datetime

# 행동 패턴 별로 사용되는 센서 조합 정의
combinations = {
    "sleep": [
        (SensorType.FINBED1, SensorType.BEDPRESS1),
        (SensorType.FINBED2, SensorType.BEDPRESS2),
        (SensorType.FINBED3, SensorType.BEDPRESS3),
    ],
    "air": [(SensorType.FINWIN, SensorType.WINDOW)],
    "light_off": [
        (
            SensorType.FINBED1,
            SensorType.BEDPRESS1,
            SensorType.FINDESK1,
            SensorType.SWIDESK1,
        ),
        (
            SensorType.FINBED1,
            SensorType.BEDPRESS1,
            SensorType.FINDESK2,
            SensorType.SWIDESK2,
        ),
        (
            SensorType.FINBED1,
            SensorType.BEDPRESS1,
            SensorType.FINDESK3,
            SensorType.SWIDESK3,
        ),
        (
            SensorType.FINBED2,
            SensorType.BEDPRESS2,
            SensorType.FINDESK1,
            SensorType.SWIDESK1,
        ),
        (
            SensorType.FINBED2,
            SensorType.BEDPRESS2,
            SensorType.FINDESK2,
            SensorType.SWIDESK2,
        ),
        (
            SensorType.FINBED2,
            SensorType.BEDPRESS2,
            SensorType.FINDESK3,
            SensorType.SWIDESK3,
        ),
        (
            SensorType.FINBED3,
            SensorType.BEDPRESS3,
            SensorType.FINDESK1,
            SensorType.SWIDESK1,
        ),
        (
            SensorType.FINBED3,
            SensorType.BEDPRESS3,
            SensorType.FINDESK2,
            SensorType.SWIDESK2,
        ),
        (
            SensorType.FINBED3,
            SensorType.BEDPRESS3,
            SensorType.FINDESK3,
            SensorType.SWIDESK3,
        ),
    ],
}
items = list(combinations.items())


def analyze():
    print("Starting analysis...")
    while True:  # 무한 루프 - 항상 센서 상태를 감시
        for sensor in sensors:
            sensor.update()
        for pattern, combs in items:
            for comb in combs:  # 가능한 센서 조합별로 확인
                sgn = 2
                inputs = []  # 센서 값 수집 리스트

                # 센서 조합의 각 센서에 대해 유효한 변화가 있는지 확인
                for sensor_id in comb:
                    sensor = sensors[int(sensor_id)]

                    if not sensor.is_valid() or (
                        not sensor.ignore_sgn and sgn != 2 and sgn != sensor.get_sgn()
                    ):
                        break
                    else:
                        inputs.append(sensor.input)  # 센서 값 수집
                        sgn = sensor.get_sgn()
                else:
                    # 첫 번째 센서 값을 기반으로 사용자 이메일 구성
                    email = f"{inputs[0]}@sshs.hs.kr"
                    user = users.find_one({"email": email})

                    if not user:
                        continue

                    # 시간 기반 패턴 처리
                    if pattern in TIME_PATTERNS:
                        new_patterns = user["patterns"]

                        # 현재 시간 기록
                        new_patterns[pattern].append(
                            datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
                            + ("+A" if sgn > 0 else "-A")
                        )
                        users.update_one(
                            {"email": email}, {"$set": {"patterns": new_patterns}}
                        )
                        print(f"Added pattern {pattern} to {user['username']}")
                    elif pattern == OFF_PATTERN:
                        new_patterns = user["patterns"]
                        new_patterns[pattern].append(
                            datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
                            + str(inputs[-1])
                        )
                        users.update_one(
                            {"email": email}, {"$set": {"patterns": new_patterns}}
                        )
                        print(f"Added pattern {pattern} to {user['username']}")
