from matcher.utils.scoring_utils import ScoringService
from matcher.services.matching_service import MatchingService
from matcher.ui.matcher_window import MatcherWindow


def start(root):
    scoring_service = ScoringService()
    matching_service = MatchingService(scoring_service)

    root.title("룸메이트 매칭 시스템")

    matcher_window = MatcherWindow(root, matching_service)
    matcher_window.show_password_verification()
