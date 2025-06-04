from utils.base_window import BaseWindow
from share.ui.auth_window import AuthWindow
from utils.button import Button


class MainWindow(BaseWindow):
    def __init__(self, root):
        super().__init__(root)
        self.auth_windows = AuthWindow(root)
        self.show_main_menu()

    def show_main_menu(self, show_password_find=True):
        """메인 메뉴 표시"""
        self.root.title("패턴 공유 플랫폼")

        login_button = Button(
            self.root,
            text="로그인",
            command=lambda: self.auth_windows.show_login(
                [login_button, signup_button],
                (password_find_button if show_password_find else None),
            ),
        )
        login_button.pack()

        signup_button = Button(
            self.root,
            text="회원가입",
            command=lambda: self.auth_windows.show_signup(
                [login_button, signup_button]
            ),
        )
        signup_button.pack()

        if show_password_find:
            password_find_button = Button(
                self.root,
                text="비밀번호 찾기",
                command=lambda: self.auth_windows.show_password_reset(
                    [login_button, signup_button, password_find_button]
                ),
            )
            password_find_button.pack(anchor="w")

        self.widgets = [login_button, signup_button] + (
            [password_find_button] if show_password_find else []
        )
