
import time
import os
import pyautogui
import pydirectinput

# 从环境变量读取密码，避免直接写入源代码
# ANDROID_PIN = os.environ["ANDROID_PIN"]

class DeskflowScreenSwitcher:
    def __init__(self):
        self.screen_direction = "left"  # 默认切换方向
        self.DIRECTIONS = ["left", "up", "right", "down"]
        # 内部变量
        self.__x = 0
        self.__y = 0
        self.__delta_x = 0
        self.__delta_y = 0



    def switch_to(self, direction: str = "left"):
        width, height = pyautogui.size()
        print(width, height)
        if direction == "left":
            self.__x = 0
            self.__y = height // 2
            self.__delta_x = -20
            self.__delta_y = 0
        elif direction == "right":
            self.__x = width - 1
            self.__y = height // 2
            self.__delta_x = 20
            self.__delta_y = 0
        elif direction == "up":
            self.__x = width // 2
            self.__y = 0
            self.__delta_x = 0
            self.__delta_y = -20
        elif direction == "down":
            self.__x = width // 2
            self.__y = height - 1
            self.__delta_x = 0
            self.__delta_y = 20

        print(f"Moving mouse to ({self.__x}, {self.__y})")
        pyautogui.moveTo(self.__x, self.__y, duration=0)
        time.sleep(0.2)

        # 注入相对鼠标移动事件，切入对应屏幕
        for _ in range(1):
            pydirectinput.moveRel(self.__delta_x, self.__delta_y, relative=True)
            time.sleep(0.03)




    def switch_back(self):
        # 返回主屏幕
        for _ in range(1):
            pydirectinput.moveRel(-2 * self.__delta_x, -2 * self.__delta_y, relative=True)
            time.sleep(0.03)

        pyautogui.moveTo(800, 500, duration=0) 

        pyautogui.write("Hello, World!", interval=0.1)
        pyautogui.press("enter")

    def terminal_unlock(self, unlock_pin: str):
        # 1. 唤醒终端
        pyautogui.press("space")
        time.sleep(0.5)

        # 2. 输入 PIN 解锁
        pyautogui.write(unlock_pin, interval=0.1)
        pyautogui.press("enter")
        time.sleep(1.0)

if __name__ == "__main__":
    dss = DeskflowScreenSwitcher()
    dss.switch_to("down")
    
    unlock_pin = os.environ["ANDROID_PIN"]
    dss.terminal_unlock(unlock_pin)
    
    dss.switch_back()
