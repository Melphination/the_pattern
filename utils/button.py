from tkinter import ttk
import tkinter as tk
from nava import play
from utils.resource_path import resource_path


class Button(ttk.Button):
    def __init__(self, root: tk.Tk, **kwargs):
        """
        커스텀 버튼 클래스
        클릭 시 사운드를 재생한 후 원래 command 실행
        """
        self.command = kwargs.get("command", lambda: None)  # 원래의 command를 별도 저장
        kwargs["command"] = self.press  # 버튼 클릭 시 press() 실행되도록 설정
        super().__init__(root, **kwargs)

    def press(self):
        # 사운드 재생
        try:
            play(resource_path("sounds/button.mp3"))
        except Exception as e:
            print(f"Sound play failed: {e}")

        # 원래의 command 실행
        self.command()
