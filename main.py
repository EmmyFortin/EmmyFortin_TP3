import os
import sys

absolute_file_path = os.path.abspath(__file__)
absolute_folder_path = os.path.dirname(absolute_file_path)

sys.path.append(absolute_folder_path)

# refresh des fichiers
import importlib
import ui
import animator

importlib.reload(animator)
importlib.reload(ui)


def main():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    tool_window = ui.RandomAnimatorGenerator()
    tool_window.show()

main()