import animator
import ui


def main():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    tool_window = ui.RandomAnimatorGenerator()
    tool_window.show()

main()