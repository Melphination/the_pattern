from datetime import datetime
import secrets, os, smtplib, string
from email.mime.text import MIMEText
from dotenv import load_dotenv
from typing import List


load_dotenv()
charset = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")


# 안전한 비밀번호인지 판단하는 함수
def safety_check(pw: str) -> bool:
    return (
        len(pw) >= 8
        and sum(int(c.isupper()) for c in pw) >= 2
        and sum(int(c.islower()) for c in pw) >= 2
        and sum(int(c.isdigit()) for c in pw) >= 2
    )


def valid_id(id: str) -> bool:
    return len(set(id) - charset) == 0


# 휴학생 등의 특별한 사람들의 교번은 special에 저장
special = [22092]


# 가능한 교번 반환
def possible_number() -> List[int]:
    last = datetime.now().year % 100
    # 3월 1일부터는 신입생 들어옴 가정
    if datetime.today().strftime("%m-%d") < "03-01":
        last -= 1
    return special + list(range((last - 2) * 1000 + 1, (last + 1) * 1000))


# 재학생이 맞는지 이메일 형식이 맞는지 확인
# 형식이 맞으면 1 리턴, 틀리면 -1 리턴
def email_format_check(email: str) -> bool:
    if len(email) != 16 or not email.endswith("@sshs.hs.kr"):
        return False
    if int(email[:5]) in possible_number():
        return True
    return False


N = 8
possible_chars = string.ascii_letters + string.digits


# 이메일 인증을 위한 코드 생성
def gen_code() -> str:
    return "".join(secrets.choice(possible_chars) for _ in range(N))


# 이메일 인증
sender = os.environ["NAVER_MAIL"]
password = os.environ["NAVER_PW"]


def send_verify_email(receipt) -> str:
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
    code = gen_code()
    msg = MIMEText(code)
    msg["Subject"] = "THE PATTERN 비밀번호 재설정"
    msg["From"] = sender
    msg["To"] = receipt
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, receipt, msg.as_string())
    return code
