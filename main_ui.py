import tkinter as tk
from tkinter import ttk
from utils.restart import back_to_menu
from utils.button import Button
import sys
from utils.resource_path import resource_path


def main_ui():
    try:
        # Tkinter 루트 윈도우 생성
        root = tk.Tk()
        root.title("THE PATTERN")
        root.iconbitmap(resource_path("images/logo.ico"))  # 앱 아이콘 설정

        # 로고 이미지 표시
        imgtk = tk.PhotoImage(file=resource_path("images/logo.png"))
        panel = ttk.Label(root, image=imgtk)
        panel.pack()

        # 메인 메뉴 버튼
        menu_button = Button(root, text="메인 메뉴", command=back_to_menu)
        menu_button.pack(anchor="w")

        # 모드 선택을 위한 변수 (기본값: 매칭 시스템)
        mode = tk.StringVar(root, value="매칭 시스템")

        # 모드 확인 시 호출되는 함수
        def check(mode):
            panel.pack_forget()
            mode_options.pack_forget()
            mode_button.pack_forget()

            # 선택된 모드에 따라 다음 동작 수행
            match mode.get():
                case "공유 플랫폼":
                    from share.share import start

                    start(root)
                case "매칭 시스템":
                    from matcher.matcher import start

                    start(root)
                case _:
                    raise Exception(f"Unknown mode {mode.get()}")

        # 모드 선택 드롭다운 메뉴 생성
        # (주의: 매칭 시스템을 기본값으로 넣지 않으면 드롭다운에서 사라지는 버그 발생)
        mode_options = ttk.OptionMenu(
            root, mode, "매칭 시스템", "매칭 시스템", "공유 플랫폼"
        )
        mode_options.pack()

        mode_button = Button(root, text="확인", command=lambda: check(mode))
        mode_button.pack()

        # 창 크기 설정
        root.geometry("1000x1000")

        # 메인 이벤트 루프 시작
        root.mainloop()
    except Exception as e:
        # 예외 발생 시 GUI 종료 및 에러 출력
        root.destroy()
        print(e)
        sys.exit()
