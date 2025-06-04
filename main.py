from main_ui import main_ui
from analysis.analyze import analyze
import sys
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        multiprocessing.Process(target=analyze).start()
        main_ui()
    except KeyboardInterrupt:
        sys.exit()
