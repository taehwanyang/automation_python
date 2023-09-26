import pyautogui
import pyperclip

def write(s):
    pyperclip.copy(s)
    pyautogui.hotkey('command', 'v')


