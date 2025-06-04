import os, sys


def back_to_menu():
    """메인 화면으로 되돌아가기"""
    os.execl(sys.executable, sys.executable, "main.py")
