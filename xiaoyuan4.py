import cv2
import numpy as np
import pyautogui
import pytesseract
import keyboard
import sys
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

not_found_count = 0
last_not_found_time = 0
last_numbers = None  # 用于存储上次识别的数字
skip_count = 0  # 跳过次数计数器
skiptime = 0.1

# def capture_area():
#     region = (284, 3。36, 400, 100) 
#     screenshot = pyautogui.screenshot(region=region)
#     return np.array(screenshot)

def capture_area():
    # 定义两个不同的区域
    region1 = (220, 300, 100, 100)  # 第一个数字的区域
    region2 = (400, 300, 100, 100)  # 第二个数字的区域
    screenshot1 = pyautogui.screenshot(region=region1)
    screenshot2 = pyautogui.screenshot(region=region2)
    screenshot1.save('screenshot1.png')
    screenshot2.save('screenshot2.png')

    return np.array(screenshot1), np.array(screenshot2)

# def recognize_numbers(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#     text = pytesseract.image_to_string(thresh, config='--psm 6')
#     numbers = [int(s) for s in text.split() if s.isdigit()]
#     return numbers

def recognize_numbers(image1, image2):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    _, thresh1 = cv2.threshold(gray1, 150, 255, cv2.THRESH_BINARY)
    
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    _, thresh2 = cv2.threshold(gray2, 150, 255, cv2.THRESH_BINARY)
    
    text1 = pytesseract.image_to_string(thresh1, config='--psm 6')
    text2 = pytesseract.image_to_string(thresh2, config='--psm 6')
    
    numbers1 = [int(s) for s in text1.split() if s.isdigit()]
    numbers2 = [int(s) for s in text2.split() if s.isdigit()]
    
    return numbers1, numbers2

# def draw_comparison(numbers):
def draw_comparison(numbers1, numbers2):
    global not_found_count, last_not_found_time, last_numbers, skip_count

    numbers = (numbers1, numbers2)
    # if len(numbers) < 2:
    if len(numbers1) != 1 or len(numbers2) != 1:
        current_time = time.time()
        if not_found_count == 0 or current_time - last_not_found_time > 1:
            not_found_count = 1
        else:
            not_found_count += 1
        
        last_not_found_time = current_time
        print("No data found for comparison")
        
        if not_found_count >= 8:
            # pyautogui.click(280, 840)  # 点击“开心收下”按钮
            pyautogui.click(250, 680)
            time.sleep(0.3)
            # pyautogui.click(410, 990)  # 点击“继续”按钮
            pyautogui.click(410, 1200)
            time.sleep(2)
            # pyautogui.click(280, 910)  # 点击“继续PK”按钮
            pyautogui.click(280, 1100)
            time.sleep(10)
            print("Preparing to start over...")
            time.sleep(0.3)
            main()
        return

    if last_numbers is not None and last_numbers == numbers:
        skip_count += 1
        print(f"The current result is the same as last time, skip this execution (Times: {skip_count})")
        
        if skip_count > 2:  # 超过5次则强制执行一次
            skip_count = 0  # 重置计数器
            print("Skip more than 2 times, enforce once")
            # 在这里可以直接执行绘制逻辑，或根据需要处理
            # first, second = numbers1[0], numbers2[0]
            first, second = numbers1[0], numbers2[0]
            origin_x, origin_y = 250, 650  # 绘制区域坐标
            size = 50
            
            if first > second:
                print(f"{first} > {second}")
                draw_greater_than(origin_x, origin_y, size)
            elif first < second:
                print(f"{first} < {second}")
                draw_less_than(origin_x, origin_y, size)
        return

    first, second = numbers1[0], numbers2[0]
    origin_x, origin_y = 250, 650  # 绘制区域坐标
    size = 50

    if first > second:
        print(f"{first} > {second}")
        draw_greater_than(origin_x, origin_y, size)
    elif first < second:
        print(f"{first} < {second}")
        draw_less_than(origin_x, origin_y, size)

    not_found_count = 0  
    last_numbers = numbers  # 更新 last_numbers 为当前数字
    skip_count = 0  # 重置跳过次数

def draw_greater_than(origin_x, origin_y, size):
    pyautogui.press(".") 

def draw_less_than(origin_x, origin_y, size):
    pyautogui.press(",") 

def main():
    keyboard.add_hotkey('=', lambda: sys.exit("Process has ended"))  # 默认退出快捷键是 "="

    try:
        while True:
            # image = capture_area()
            # numbers = recognize_numbers(image)
            # draw_comparison(numbers)
                # 获取两个区域的截图
            image1, image2 = capture_area()

             # 识别两个区域中的数字
            numbers1, numbers2 = recognize_numbers(image1, image2)

    # 进行数字比较和绘制
            draw_comparison(numbers1, numbers2)
            time.sleep(skiptime)  
    except SystemExit as e:
        print(e)
# 示例绘制函数
# def draw_greater_than(x, y, size):
#     pass

# def draw_less_than(x, y, size):
#     pass

if __name__ == "__main__":
    main()
