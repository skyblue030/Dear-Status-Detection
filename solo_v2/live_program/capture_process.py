import cv2
import numpy as np
import os
import time
import threading
import queue
from tkinter import Tk, Canvas
from PIL import Image, ImageTk
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def send_line_notify(message, token):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "message": message
    }
    response = requests.post(url, headers=headers, data=data)
    return response


token = os.environ.get("LINE_NOTIFY_TOKEN")
message = "這是一則來自 VS Code 的通知訊息"





# 全局变量，用于线程间通信
frame_queue = queue.Queue()
difference_queue = queue.Queue()

# 终止标志
terminate_flag = threading.Event()

# 录制区域
recording_area = None
drawing = False
ix, iy = -1, -1

# 防止 ImageTk.PhotoImage 对象被垃圾回收
imgtk_cache = None

def select_area(event):
    global ix, iy, drawing, recording_area
    if event.type == '4':  # Mouse button pressed
        drawing = True
        ix, iy = event.x, event.y
    elif event.type == '6' and drawing:  # Mouse movement
        recording_area = (ix, iy, event.x, event.y)
        canvas.delete("rectangle")
        canvas.create_rectangle(ix, iy, event.x, event.y, outline='green', width=2, tag="rectangle")
    elif event.type == '5':  # Mouse button released
        drawing = False
        x1, y1, x2, y2 = ix, iy, event.x, event.y
        recording_area = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        print(f"Selected area: {recording_area}")

# 摄像头捕获程序
def capture_videos_from_camera():
    cap = cv2.VideoCapture(0)  # 打开默认摄像头
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    prev_frame = None

    while not terminate_flag.is_set():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame from camera.")
            continue

        # 打印帧的形状以进行调试


        # 将帧放入队列
        if not frame_queue.full():
            frame_queue.put(frame)

        # 计算像素差值
        if prev_frame is not None and recording_area:
            x1, y1, x2, y2 = recording_area
            # 确保区域在图像范围内
            if x1 >= 0 and y1 >= 0 and x2 <= frame.shape[1] and y2 <= frame.shape[0]:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cropped_gray = gray[y1:y2, x1:x2]
                cropped_prev_frame = prev_frame[y1:y2, x1:x2]
                diff = cv2.absdiff(cropped_prev_frame, cropped_gray)
                diff_sum = np.sum(diff)

                # 将差值放入差值队列
                if not difference_queue.full():
                    difference_queue.put(diff_sum)
            else:
                print("Selected area is out of frame bounds")
                print(f"Frame shape: {frame.shape}, Recording area: {recording_area}")

        prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cap.release()
    print("Capture thread terminated.")

# 显示摄像头画面的程序
def display_camera():
    global canvas, image_on_canvas, imgtk_cache
    root = Tk()
    root.title("Camera Feed")
    canvas = Canvas(root, width=640, height=480)
    canvas.pack()

    canvas.bind("<ButtonPress-1>", select_area)
    canvas.bind("<B1-Motion>", select_area)
    canvas.bind("<ButtonRelease-1>", select_area)

    image_on_canvas = None

    def update_frame():
        global image_on_canvas, imgtk_cache
        if not frame_queue.empty():
            frame = frame_queue.get()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            imgtk_cache = imgtk  # 防止被垃圾回收
            if image_on_canvas is None:
                image_on_canvas = canvas.create_image(0, 0, anchor='nw', image=imgtk)
            else:
                canvas.itemconfig(image_on_canvas, image=imgtk)
 

        if not terminate_flag.is_set():
            canvas.after(30, update_frame)  # 调整更新频率
        else:
            root.destroy()

    update_frame()
    root.mainloop()
    print("Display thread terminated.")

# 状态判断程序
def classify_differences(differences, low_threshold, high_threshold):
    state_counts = {"Aggressive": 0, "Normal": 0, "Passive": 0}
    for diff in differences:
        if diff is None:
            continue
        if diff >= high_threshold:
            state_counts["Aggressive"] += 1
            
        elif diff >= low_threshold:
            state_counts["Normal"] += 1
        else:
            state_counts["Passive"] += 1

    total_counts = sum(state_counts.values())
    if total_counts == 0:
        return 'Unknown'

    for state, count in state_counts.items():
        percentage = (count / total_counts) * 100
        if percentage > 75:
            return state

    return 'Normal'  # 如果没有任何状态超过75%，则返回'Normal'

def process_differences(low_threshold, high_threshold):
    while not terminate_flag.is_set():
        differences = []
        start_time = time.time()

        # 5秒内收集差值数据
        while time.time() - start_time < 5:
            if not difference_queue.empty():
                diff = difference_queue.get()
                differences.append(diff)
            time.sleep(1)  # 每秒钟收集一次

        # 打印收集到的差值数组
  

        if differences:
            state = classify_differences(differences, low_threshold, high_threshold)
            print(f"State: {state}")
            if state == "Aggressive":
                response = send_line_notify(message, token)
                if response.status_code == 200:
                    print("訊息發送成功")
                else:
                    print("訊息發送失敗:", response.text)

    print("Process thread terminated.")

# 假设阈值已经被加载
low_threshold = 10000  # 假设这些值已经定义
high_threshold = 500000

# 创建线程
capture_thread = threading.Thread(target=capture_videos_from_camera)
process_thread = threading.Thread(target=process_differences, args=(low_threshold, high_threshold))
display_thread = threading.Thread(target=display_camera)

# 启动线程
capture_thread.start()
process_thread.start()
display_thread.start()

# 等待用户中断（例如通过按下Ctrl+C）
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminating threads...")
    terminate_flag.set()

# 等待线程完成
capture_thread.join()
process_thread.join()
display_thread.join()

print("All threads terminated.")
