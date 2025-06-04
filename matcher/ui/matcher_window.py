import tkinter as tk
from tkinter import ttk
from tksheet import Sheet
from typing import Optional
from utils.verify_admin import verify_admin
from utils.button import Button
from utils.base_window import BaseWindow
from utils.connect_db import rooms as rooms_db


class MatcherWindow(BaseWindow):
    def __init__(
        self,
        root: tk.Tk,
    ):
        super().__init__(root)
        self.progress_bar: Optional[ttk.Progressbar] = None

    def show_password_verification(self):
        """비밀번호 인증 화면 표시"""
        pw_label = ttk.Label(self.root, text="비밀번호")
        pw_label.pack()

        pw_var = tk.StringVar()
        pw_entry = ttk.Entry(self.root, textvariable=pw_var, show="*")
        pw_entry.pack()

        confirm_button = Button(
            self.root,
            text="확인",
            command=lambda: self.verify_password(
                pw_var, [pw_label, pw_entry, confirm_button]
            ),
        )
        confirm_button.pack()

    def show_main_interface(self):
        """메인 인터페이스 표시"""
        # 매칭 실행 버튼
        match_button = Button(
            self.root, text="새로운 룸메이트 매칭?", command=self.start_matching
        )
        match_button.pack()

        # 현재 방 배정 현황 테이블
        self.create_rooms_table()

        # 진행률 표시 바
        self.create_progress_bar()

    def verify_password(self, password_var: tk.StringVar, widgets_to_destroy: list):
        """비밀번호 검증 처리"""
        self.clear_widgets(widgets_to_destroy)

        if verify_admin(password_var.get()):
            self.show_main_interface()
        else:
            self.show_error("비밀번호가 틀렸습니다.")

    def start_matching(self):
        """매칭 시작"""
        if not self.progress_bar:
            return

        self.progress_bar["value"] = 0

        # 매칭 실행
        matched_pairs = self.matching_service.execute_matching(
            self.root, self.progress_bar
        )

        # 방 배정
        self.matching_service.assign_rooms(matched_pairs, self.progress_bar, self.root)

        self.show_error("Matching finished")

        # 테이블 새로고침
        self.refresh_rooms_table()

    def create_rooms_table(self):
        """방 배정 현황 테이블 생성"""
        rooms = rooms_db.find()
        table_data = [
            [
                room.number,
                *[student.get("username", "") for student in room["students"]],
            ]
            for room in rooms
        ]

        self.rooms_sheet = Sheet(
            self.root,
            data=table_data,
            height=520,
            width=1000,
        )
        self.rooms_sheet.pack()

    def create_progress_bar(self):
        """진행률 표시 바 생성"""
        self.progress_bar = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=200,
            mode="determinate",
            maximum=100,
            takefocus=True,
            value=0,
        )
        self.progress_bar.pack()

    def refresh_rooms_table(self):
        """테이블 새로고침"""
        if hasattr(self, "rooms_sheet"):
            rooms = rooms_db.find()
            table_data = [
                [
                    room.number,
                    *[student.get("username", "") for student in room["students"]],
                ]
                for room in rooms
            ]
            self.rooms_sheet.set_sheet_data(table_data)
