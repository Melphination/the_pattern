from tkinter import ttk
import tkinter as tk


class BaseWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.widgets = []
        self.error_labels = []

    def clear_widgets(self, widgets=None):
        """위젯 제거"""
        widgets_to_clear = widgets or self.widgets
        for widget in widgets_to_clear:
            widget.destroy()

    def clear_errors(self):
        """에러 메시지 제거"""
        for label in self.error_labels:
            label.destroy()
        self.error_labels.clear()

    def show_error(self, message):
        """에러 메시지 표시"""
        self.clear_errors()
        error_label = ttk.Label(self.root, text=message, wraplength=300, justify="center")
        error_label.pack(anchor="w")
        self.error_labels.append(error_label)
