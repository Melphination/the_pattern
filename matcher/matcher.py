from matcher.ui.matcher_window import MatcherWindow


def start(root):
    root.title("룸메이트 매칭 시스템")

    matcher_window = MatcherWindow(root)
    matcher_window.show_password_verification()
