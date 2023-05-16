import pyautogui as agent
import webbrowser as chrome
import time

chrome.open('{url}')
time.sleep(10)
signup_pos = agent.locateCenterOnScreen('signup.png')
print(signup_pos)
# Because this labtop is macbook 
agent.moveTo(signup_pos.x/2, signup_pos.y/2, duration=3)
agent.click()