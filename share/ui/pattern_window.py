from tksheet import Sheet
from utils.base_window import BaseWindow
from utils.button import Button
from share.utils.pattern_utils import (
    get_user_patterns_display,
    get_roommate_patterns_display,
    save_patterns,
)


class PatternWindow(BaseWindow):
    def __init__(self, root):
        super().__init__(root)

    def show_patterns(self, username):
        """패턴 공유 화면 표시"""
        self.root.title(f"패턴 공유 플랫폼 - {username}")

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
            height=520,
            width=500,
            default_column_width=500,
        )
        user_sheet.enable_bindings("all")
        user_sheet.pack()

        # 룸메이트 패턴 시트
        roommates, roommate_patterns = get_roommate_patterns_display(username)

        if roommates:
            roommate_sheet = Sheet(
                self.root,
                data=[roommates] + roommate_patterns,
                height=520,
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
