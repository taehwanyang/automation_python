import pyautogui

def write(s):
    import pyperclip
    pyperclip.copy(s)
    pyautogui.hotkey('command', 'v')


