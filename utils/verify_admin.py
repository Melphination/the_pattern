import argon2
import os
from dotenv import load_dotenv

load_dotenv()
ph = argon2.PasswordHasher()


def verify_admin(pw: str) -> bool:
    """관리자 비밀번호 검증"""
    try:
        admin_hash = os.environ["ADMIN_PW"]
        ph.verify(admin_hash, pw)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False
