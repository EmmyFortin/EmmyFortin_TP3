import os
import sys

absolute_file_path = os.path.abspath(__file__)
absolute_folder_path = os.path.dirname(absolute_file_path)

sys.path.append(absolute_folder_path)

# refresh des fichiers
import importlib
import ui
import animator

importlib.reload(ui)
importlib.reload(animator)



def main():
    global animator_tool_window

    try:
        animator_tool_window.close()
    except Exception:
        pass

    animator_tool_window = ui.RandomAnimatorGenerator()
    animator_tool_window.show()

main()