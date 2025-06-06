import tkinter as tk
from tkinter import ttk
from utils.base_window import BaseWindow
from utils.button import Button
from utils.restart import back_to_menu
from utils.connect_db import rooms
from share.ui.pattern_window import PatternWindow
import argon2
from share.utils.auth_utils import register_user, validate_signup_data
from share.utils.user_utils import authenticate
from utils.verification import send_pw_email, send_verify_email
from utils.connect_db import users
from datetime import datetime, timedelta


class AuthWindow(BaseWindow):
    def __init__(self, root):
        super().__init__(root)
        self.ph = argon2.PasswordHasher()

    def show_login(self, previous_widgets=None, password_find_button=None):
        """로그인 화면 표시"""
        if previous_widgets:
            self.clear_widgets(previous_widgets)

        self.root.title("패턴 공유 플랫폼 - 로그인")

        username_var = tk.StringVar(self.root)
        password_var = tk.StringVar(self.root)

        username_label = ttk.Label(self.root, text="아이디")
        username_label.pack()
        username_entry = ttk.Entry(self.root, textvariable=username_var)
        username_entry.pack()

        password_label = ttk.Label(self.root, text="비밀번호")
        password_label.pack()
        password_entry = ttk.Entry(self.root, textvariable=password_var, show="*")
        password_entry.pack()

        login_button = Button(
            self.root,
            text="로그인",
            command=lambda: self.handle_login(
                username_var,
                password_var,
                [
                    username_label,
                    username_entry,
                    password_label,
                    password_entry,
                    login_button,
                ]
                + ([password_find_button] if password_find_button else []),
            ),
        )
        login_button.pack()

        self.widgets = [
            username_label,
            username_entry,
            password_label,
            password_entry,
            login_button,
        ] + ([password_find_button] if password_find_button else [])

    def handle_login(self, username_var, password_var, widgets):
        """로그인 처리"""
        username = username_var.get()
        password = password_var.get()

        if authenticate(username, password):
            self.clear_widgets(widgets)
            self.clear_errors()
            pattern_window = PatternWindow(self.root)
            pattern_window.show_patterns(username)
        else:
            self.show_error("비밀번호나 아이디가 틀렸습니다.")

    def show_signup(self, previous_widgets=None):
        """회원가입 화면 표시"""
        if previous_widgets:
            for widget in previous_widgets:
                widget.pack_forget()

        self.root.title("패턴 공유 플랫폼 - 회원가입")

        email_var = tk.StringVar(self.root)
        username_var = tk.StringVar(self.root)
        password_var = tk.StringVar(self.root)
        password_check_var = tk.StringVar(self.root)
        gender_var = tk.StringVar(self.root, value="M")
        grade_var = tk.StringVar(self.root, value="1")
        room_var = tk.StringVar(self.root)

        email_label = ttk.Label(self.root, text="이메일")
        email_label.pack()
        email_entry = ttk.Entry(self.root, textvariable=email_var)
        email_entry.pack()

        username_label = ttk.Label(self.root, text="아이디")
        username_label.pack()
        username_entry = ttk.Entry(self.root, textvariable=username_var)
        username_entry.pack()

        password_label = ttk.Label(self.root, text="비밀번호")
        password_label.pack()
        password_entry = ttk.Entry(self.root, textvariable=password_var, show="*")
        password_entry.pack()

        password_check_label = ttk.Label(self.root, text="비밀번호를 다시 입력하세요.")
        password_check_label.pack()
        password_check_entry = ttk.Entry(
            self.root, textvariable=password_check_var, show="*"
        )
        password_check_entry.pack()

        gender_label = ttk.Label(self.root, text="성별")
        gender_label.pack()
        gender_entry = ttk.OptionMenu(self.root, gender_var, "M", "M", "F")
        gender_entry.pack()

        grade_label = ttk.Label(self.root, text="학년")
        grade_label.pack()
        grade_entry = ttk.OptionMenu(self.root, grade_var, "1", "1", "2", "3")
        grade_entry.pack()

        room_label = ttk.Label(self.root, text="방 번호")
        room_label.pack()
        room_entry = ttk.Entry(self.root, textvariable=room_var)
        room_entry.pack()

        signup_button = Button(
            self.root,
            text="회원가입",
            command=lambda: self.handle_signup_verification(
                email_var,
                username_var,
                password_var,
                password_check_var,
                gender_var,
                grade_var,
                room_var,
                [
                    email_label,
                    email_entry,
                    username_label,
                    username_entry,
                    password_label,
                    password_entry,
                    password_check_label,
                    password_check_entry,
                    signup_button,
                    gender_label,
                    gender_entry,
                    grade_label,
                    grade_entry,
                    room_label,
                    room_entry,
                ],
            ),
        )
        signup_button.pack()

        self.widgets = [
            email_label,
            email_entry,
            username_label,
            username_entry,
            password_label,
            password_entry,
            password_check_label,
            password_check_entry,
            signup_button,
        ]

    def handle_signup_verification(
        self,
        email_var,
        username_var,
        password_var,
        password_check_var,
        gender_var,
        grade_var,
        room_var,
        widgets,
    ):
        """회원가입 검증 및 인증 코드 전송"""
        email = email_var.get()
        username = username_var.get()
        password = password_var.get()
        password_check = password_check_var.get()

        is_valid, error_message = validate_signup_data(
            email, username, password, password_check
        )

        if not is_valid:
            self.show_error(error_message)
            return

        # 인증 코드 전송
        try:
            code = send_verify_email(email)
            self.clear_widgets(widgets)
            self.clear_errors()
            self.show_verification_code_input(
                email,
                username_var,
                password_var,
                gender_var,
                grade_var,
                room_var,
                code,
                datetime.now(),
                mode="signup",
            )
        except:
            self.show_error("인증 코드 전송 실패")

    def show_verification_code_input(
        self,
        email,
        username_var,
        password_var,
        gender_var,
        grade_var,
        room_var,
        code,
        time,
        mode="signup",
    ):
        """인증 코드 입력 화면"""
        code_var = tk.StringVar(self.root)

        code_label = ttk.Label(self.root, text="인증 코드를 입력해주세요.")
        code_label.pack()
        code_entry = ttk.Entry(self.root, textvariable=code_var)
        code_entry.pack()

        if mode == "signup":
            code_button = Button(
                self.root,
                text="인증",
                command=lambda: self.verify_signup_code(
                    email,
                    username_var,
                    password_var,
                    gender_var,
                    grade_var,
                    room_var,
                    code_var.get(),
                    code,
                    time,
                    [code_label, code_entry, code_button],
                ),
            )
        else:  # 비밀번호 재설정
            code_button = Button(
                self.root,
                text="인증",
                command=lambda: self.verify_password_reset_code(
                    email,
                    code_var.get(),
                    code,
                    time,
                    [code_label, code_entry, code_button],
                ),
            )

        code_button.pack()

    def verify_signup_code(
        self,
        email,
        username_var,
        password_var,
        gender_var,
        grade_var,
        room_var,
        entered_code,
        correct_code,
        time,
        widgets,
    ):
        """회원가입 인증 코드 검증"""
        self.clear_widgets(widgets)

        if entered_code != correct_code:
            self.show_error("인증 코드가 틀렸습니다.")
        elif not rooms.find({"number": room_var.get()}):
            self.show_error("존재하지 않는 방 번호입니다.")
        elif datetime.now() - time > timedelta(minutes=10):
            self.show_error("인증 시간이 만료되었습니다.")
        else:
            success, error_message = register_user(
                email,
                username_var.get(),
                password_var.get(),
                gender_var.get(),
                int(grade_var.get()),
                int(room_var.get()),
            )
            if success:
                back_to_menu()
            else:
                self.show_error(error_message)

    def show_password_reset(self, previous_widgets=None):
        """비밀번호 찾기 화면"""
        if previous_widgets:
            self.clear_widgets(previous_widgets)

        email_var = tk.StringVar()

        email_label = ttk.Label(self.root, text="이메일을 입력해주세요.")
        email_label.pack()
        email_entry = ttk.Entry(self.root, textvariable=email_var)
        email_entry.pack()

        email_button = Button(
            self.root,
            text="확인",
            command=lambda: self.handle_password_reset_request(
                email_var.get(), [email_label, email_entry, email_button]
            ),
        )
        email_button.pack()

    def handle_password_reset_request(self, email, widgets):
        """비밀번호 재설정 요청 처리"""
        try:
            code = send_pw_email(email)
            self.clear_widgets(widgets)
            self.show_verification_code_input(
                email,
                None,
                None,
                None,
                None,
                None,
                code,
                datetime.now(),
                mode="password_reset",
            )
        except:
            self.show_error("인증 코드 전송 실패")

    def verify_password_reset_code(
        self, email, entered_code, correct_code, time, widgets
    ):
        """비밀번호 재설정 인증 코드 검증"""
        self.clear_widgets(widgets)

        if entered_code != correct_code:
            self.show_error("인증 코드가 틀렸습니다.")
        elif datetime.now() - time > timedelta(minutes=10):
            self.show_error("인증 시간이 만료되었습니다.")
        else:
            self.show_new_password_input(email)

    def show_new_password_input(self, email):
        """새 비밀번호 입력 화면"""
        password_var = tk.StringVar()

        password_label = ttk.Label(self.root, text="새 비밀번호를 입력하세요.")
        password_label.pack()
        password_entry = ttk.Entry(self.root, textvariable=password_var, show="*")
        password_entry.pack()

        password_button = Button(
            self.root,
            text="확인",
            command=lambda: self.handle_password_change(email, password_var.get()),
        )
        password_button.pack()

    def handle_password_change(self, email, new_password):
        """비밀번호 변경 처리"""
        try:
            users.update_one(
                {"email": email}, {"$set": {"pw": self.ph.hash(new_password)}}
            )
            back_to_menu()
        except:
            self.show_error("비밀번호 변경 실패")
