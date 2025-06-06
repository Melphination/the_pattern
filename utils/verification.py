from datetime import datetime
import secrets, os, smtplib, string
from email.mime.text import MIMEText
from dotenv import load_dotenv
from typing import Set


load_dotenv()
charset = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")


def safety_check(pw: str) -> bool:
    """비밀번호 안전성 검사"""
    return (
        len(pw) >= 8
        and sum(int(c.isupper()) for c in pw) >= 2
        and sum(int(c.islower()) for c in pw) >= 2
        and sum(int(c.isdigit()) for c in pw) >= 2
    )


def valid_id(id: str) -> bool:
    """아이디 유효성 검사"""
    return len(set(id) - charset) == 0


# 휴학생 등의 추가해야 하는 사람들의 교번
special_add = {22092}

# 휴학생 등의 제외해야 되는 사람들의 교번
special_minus = set()


def possible_number() -> Set[int]:
    """가능한 교번 반환"""
    last = datetime.now().year % 100
    # 3월 1일부터는 신입생 들어옴 가정
    if datetime.today().strftime("%m-%d") < "03-01":
        last -= 1
    return (
        special_add
        | set(range((last - 2) * 1000 + 1, (last + 1) * 1000)) - special_minus
    )


def email_format_check(email: str) -> bool:
    """이메일 형식 확인"""
    if len(email) != 16 or not email.endswith("@sshs.hs.kr"):
        return False
    if int(email[:5]) in possible_number():
        return True
    return False


N = 8
possible_chars = string.digits


def gen_code() -> str:
    """인증 코드 생성"""
    return "".join(secrets.choice(possible_chars) for _ in range(N))


# 이메일 인증
sender = os.environ["NAVER_MAIL"]
password = os.environ["NAVER_PW"]


def send_verify_email(receipt) -> str:
    """회원가입에서 이메일 인증 코드 전송"""
    code = gen_code()
    msg = MIMEText(code)
    msg["Subject"] = "THE PATTERN 인증 코드"
    msg["From"] = sender
    msg["To"] = receipt
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, receipt, msg.as_string())
    return code


def send_pw_email(receipt) -> str:
    """비밀번호 재설정을 위한 인증 코드 전송"""
    code = gen_code()
    msg = MIMEText(code)
    msg["Subject"] = "THE PATTERN 비밀번호 재설정"
    msg["From"] = sender
    msg["To"] = receipt
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, receipt, msg.as_string())
    return code
