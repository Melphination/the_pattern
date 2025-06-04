from utils.connect_db import users
from utils.pattern_types import TIME_PATTERNS, OFF_PATTERN


def combine():
    """중복된 패턴 제거"""
    for user in users.find():
        for pat in TIME_PATTERNS:
            patterns = user["patterns"][pat]

            # 문자열을 기준으로 정렬: datetime 문자열 + 끝/시작 + 패턴 추가 주체
            patterns.sort(
                key=lambda x: x[:-2]
            )  # ex: "2025:06:01:08:00:00+A"[:-2] -> 시간 기준 정렬
            i = 0
            while i < len(patterns):
                pat1 = patterns[i]
                sgn1 = pat1[-2]  # 끝/시작: '+'(시작) 또는 '-'(끝끝)
                mode1 = pat1[-1]  # 패턴 추가 주체: 'A'(시스템) 또는 'P'(사람)

                ind = i + 1
                while ind < len(patterns):
                    pat2 = patterns[ind]
                    sgn2 = pat2[-2]
                    mode2 = pat2[-1]

                    if sgn1 != sgn2:
                        break

                    # 부호와 주체가 모두 같으면 중복된 것으로 간주하여여 하나 제거
                    if sgn1 == sgn2 and mode1 == mode2:
                        # '+'일 경우 뒤에 있는 것을 제거
                        # '-'일 경우 앞에 있는 것을 제거
                        patterns.pop(ind if sgn1 == "+" else i)

                    # 부호는 같지만 모드가 다르면 우선순위에 따라 제거
                    elif sgn1 == sgn2 and mode1 != mode2:
                        if mode1 == "P":  # 'A'는 우선순위 낮음
                            patterns.pop(ind)
                        else:
                            patterns.pop(i)
                    else:
                        ind += 1
                i = ind

        # 정량값 기반 패턴은 단순히 중복 제거
        if pat == OFF_PATTERN:
            user["patterns"][pat] = list(set(user["patterns"][pat]))

        # 수정된 patterns 필드를 DB에 반영
        users.update_one(
            {"username": user["username"]}, {"$set": {"patterns": user["patterns"]}}
        )
