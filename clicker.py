import pyautogui as gui
from mss import mss
import numpy as np
import cv2
from time import sleep
import threading as th


class Clicker:
    _click = False

    def __init__(self, image_to_scan: str = "./click.png", interval=1/1000):
        self._click_image_path = image_to_scan
        self._interval = interval

    def _show_match_result(result):
        vals = cv2.minMaxLoc(result)
        print(vals)
        cv2.imshow("Result", result)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def _get_screenshot(self):
        with mss() as sct:
            sct.shot(output="screenshot.png")
        return self._get_img_gray("screenshot.png")

    def _get_img_gray(self, path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def _get_click_position(self):
        print(f"Finding match with {self._click_image_path}...")
        img = self._get_img_gray(self._click_image_path)
        screenshot = self._get_screenshot()
        result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
        # self._show_match_result(result)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("Done!")
        return (max_loc[0] + img.shape[0]/2, max_loc[1] + img.shape[1]/2)

    def _run(self):
        while self._click:
            gui.click(self._click_pos[0], self._click_pos[1])
            sleep(self._interval)

    def is_clicking(self) -> bool:
        return self._click

    def start(self):
        if self._click:
            return
        self._click = True
        self._click_pos = self._get_click_position()
        print("Clicking...")
        thread = self._run_thread = th.Thread(target=self._run)
        thread.start()

    def stop(self):
        if not self._click:
            return
        self._click = False

    def wait_for_stop(self):
        self._run_thread.join()
        print("Stopped.")
