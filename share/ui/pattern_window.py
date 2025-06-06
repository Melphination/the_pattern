from tksheet import Sheet
from utils.base_window import BaseWindow
from utils.button import Button
from tkinter import ttk
from share.utils.pattern_utils import (
    get_user_patterns_display,
    get_roommate_patterns_display,
    save_patterns,
)

description = """<포맷 설명>
기록이 있든 없든 각 패턴들은 이름 뒤에 스페이스가 무조건 있어야 한다.

sleep, air, study: 뛰어쓰기로 각 기록을 구분한다. '년:월:일:시:분:초' 형태로 시간을 입력하고, 패턴을 시작했으면 +, 끝냈으면 -를 입력하고, 마지막에 P 입력한다.
ex. 2025:05:05:23:00:00에 잠자리에 들었으면 sleep에 2025:05:05:23:00:00+P 입력

light_off: 시간을 sleep, air, study와 같이 입력하고, 잠자는 룸메이트를 위해 소등하였으면 1, 아니면 0을 입력한다.
ex. 2025:05:05:23:00:00에 룸메이트를 위해 소등하였으면, light_off에 2025:05:05:23:00:001 입력

early_bird: 0101 같이 얼리버드를 한 날에는 1, 얼리버드를 하지 않은 날에는 0을 뛰어쓰기 없이 입력
"""


class PatternWindow(BaseWindow):
    def __init__(self, root):
        super().__init__(root)

    def show_patterns(self, username):
        """패턴 공유 화면 표시"""
        self.root.title(f"패턴 공유 플랫폼 - {username}")

        # 포맷 설명
        format_label = ttk.Label(self.root, text=description, justify="center")
        format_label.pack()

        # 저장 버튼
        save_button = Button(
            self.root,
            text="저장",
            command=lambda: self.handle_save_patterns(username, user_sheet),
        )
        save_button.pack(anchor="e")

        # 사용자 패턴 시트
        user_patterns = get_user_patterns_display(username)
        user_sheet = Sheet(
            self.root,
            data=user_patterns,
            height=250,
            width=500,
            default_column_width=500,
        )
        user_sheet.enable_bindings("edit_cell")
        user_sheet.enable_bindings("column_width_resize")
        user_sheet.enable_bindings("single_select")
        user_sheet.pack()

        # 룸메이트 패턴 시트
        roommates, roommate_patterns = get_roommate_patterns_display(username)

        if roommates:
            roommate_sheet = Sheet(
                self.root,
                data=[roommates] + roommate_patterns,
                height=250,
                width=500 * len(roommates),
                default_column_width=500,
            )
            roommate_sheet.enable_bindings("column_width_resize")
            roommate_sheet.pack()

    def handle_save_patterns(self, username, sheet):
        """패턴 저장 처리"""
        # 시트 데이터를 딕셔너리 형태로 변환
        sheet_data = {}
        i = 2
        while (data := sheet[f"A{i}"].data) != "":
            sheet_data[f"A{i}"] = data
            i += 1

        success, error_message = save_patterns(username, sheet_data)
        if not success:
            self.show_error(error_message)
        else:
            self.show_error("저장되었습니다.")
