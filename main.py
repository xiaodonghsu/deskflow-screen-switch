
import time
import pyautogui
import pydirectinput

class DeskflowScreenSwitcher:
    def __init__(self):
        self.screen_direction = "left"  # 默认切换方向
        self.DIRECTIONS = ["left", "up", "right", "down"]
        # 内部变量
        self.__x = 0
        self.__y = 0
        self.__delta_x = 0
        self.__delta_y = 0
        self.delta = 20  # 每次切换的像素偏移量

    def set_direction(self, direction: str):
        if direction in self.DIRECTIONS:
            self.screen_direction = direction
        else:
            raise ValueError(f"Invalid direction: {direction}. Must be one of {self.DIRECTIONS}")
        width, height = pyautogui.size()
        if direction == "left":
            self.__x = 0
            self.__y = height // 2
            self.__delta_x = -self.delta
            self.__delta_y = 0
        elif direction == "right":
            self.__x = width - 1
            self.__y = height // 2
            self.__delta_x = self.delta
            self.__delta_y = 0
        elif direction == "up":
            self.__x = width // 2
            self.__y = 0
            self.__delta_x = 0
            self.__delta_y = -self.delta
        elif direction == "down":
            self.__x = width // 2
            self.__y = height - 1
            self.__delta_x = 0
            self.__delta_y = self.delta

    def switch_to(self, direction: str = "left"):
        self.set_direction(direction)
        pyautogui.moveTo(self.__x, self.__y, duration=0)
        time.sleep(0.1)

        # 注入相对鼠标移动事件，切入对应屏幕
        for _ in range(1):
            pydirectinput.moveRel(self.__delta_x, self.__delta_y, relative=True)
            time.sleep(0.1)

    def switch_back(self):
        # 注入相对鼠标移动事件，返回主屏幕
        for _ in range(1):
            pydirectinput.moveRel(-2 * self.__delta_x, -2 * self.__delta_y, relative=True)
            time.sleep(0.1)

    def terminal_unlock(self, unlock_pin: str):
        # 1. 唤醒终端
        pyautogui.press("space")
        time.sleep(0.5)

        # 2. 输入 PIN 解锁
        pyautogui.write(unlock_pin, interval=0.1)
        pyautogui.press("enter")
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        _ = load_dotenv()
    except ImportError:
        pass
   
    dss = DeskflowScreenSwitcher()
    # dss.switch_to("down")
    dss.switch_to("left")
    try:
        import os
        unlock_pin = os.environ["ANDROID_PIN"]
        dss.terminal_unlock(unlock_pin)
    except KeyError:
        print("Error: ANDROID_PIN environment variable not set.")
        exit(1)
    
    dss.switch_back()
    
    pyautogui.moveTo(800, 500, duration=0) 
    pyautogui.write("I'm back!", interval=0.1)
