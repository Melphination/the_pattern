from utils.verification import safety_check, valid_id, email_format_check
from share.utils.user_utils import create_user
from utils.connect_db import users


def validate_signup_data(email, username, password, password_check):
    """회원가입 데이터 유효성 검사"""
    if users.find_one({"username": username}) or users.find_one({"email": email}):
        return False, "이미 존재하는 아이디 또는 이메일입니다."
    if password != password_check:
        return False, "비밀번호가 일치하지 않습니다."

    if not safety_check(password):
        return (
            False,
            "비밀번호는 대문자, 소문자, 숫자, 기호를 모두 적어도 하나씩 포함해야 하며 8자 이상 12자 이하여야 합니다.",
        )

    if not valid_id(username):
        return False, "아이디는 알파벳 또는 _로만 이루어질 수 있습니다."

    if not email_format_check(email):
        return False, "이메일 형식이 맞지 않거나 재학생이 아닙니다."

    email_exists = users.find_one({"email": email})
    username_exists = users.find_one({"username": username})

    if email_exists or username_exists:
        return False, "이메일 또는 아이디가 중복되어 있습니다."

    return True, ""


def register_user(email, username, password, gender, grade, room):
    """사용자 등록"""
    try:
        create_user(email, username, password, gender, grade, room)
        return True, ""
    except:
        return False, "사용자 등록을 실패했습니다."
