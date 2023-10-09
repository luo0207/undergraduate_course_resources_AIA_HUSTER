import cv2
import tkinter as tk
from tkinter import *
import os
from PIL import Image, ImageTk

root_window = tk.Tk()
root_window.title("blink-detection-demo")
root_window.geometry("1200x800") #set main——window size
vedio = tk.Canvas(root_window, bg='black', height=400, width=600)
vedio.place(x=10,y=10)

# 创建状态选择按钮
status_frame = tk.Frame(root_window)
status_frame.place(relx=0.01, rely=0.7)
status_label = tk.Label(status_frame, text="请选择你接下来的状态：")
status_label.pack(padx=2,pady=10)
status = "read paper"
def set_status(value):
    status = value
read_paper_btn = tk.Radiobutton(status_frame, text="read paper", variable=status, value="read paper",command=set_status("read paper"))
read_paper_btn.pack(side=tk.LEFT)
play_game_btn = tk.Radiobutton(status_frame, text="play game", variable=status, value="play game",command=set_status("play game"))
play_game_btn.pack(side=tk.LEFT)
watch_video_btn = tk.Radiobutton(status_frame, text="watch video", variable=status, value="watch video",command=set_status("watch video"))
watch_video_btn.pack(side=tk.LEFT)
watch_video_btn = tk.Radiobutton(status_frame, text="write code", variable=status, value="write code",command=set_status("write code"))
watch_video_btn.pack(side=tk.LEFT)


# 创建开始采集按钮
def get_vedio(status):
    save_folder = "captured_videos"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 检查之前保存的视频数量，用于生成新的文件名
    status_videos = {}
    status_folder = os.path.join(save_folder, status)
    if not os.path.exists(status_folder):
        os.makedirs(status_folder)
    else:
        existing_videos = os.listdir(status_folder)
        status_videos[status] = len(existing_videos)

    video_name = f"{status}_{status_videos.get(status, 0)}.avi"
    save_path = os.path.join(status_folder, video_name)

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 获取摄像头的宽度和高度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 创建视频编码器，用于保存视频
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(save_path, fourcc, 30.0, (width, height))

    print("开始采集视频，用户选择的状态为:", status)
    while True:
        # 读取视频帧
        ret, frame = cap.read()

        if ret:
            # 显示当前帧
            cvimage = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2BGRA)
            pilImage = Image.fromarray(cvimage).resize((400,600),Image.ANTIALIAS)
            tkImage = ImageTk.PhotoImage(image=pilImage)
            vedio.create_image(image=tkImage)
            # cv2.imshow('Frame', frame)

            # 保存当前帧到视频文件
            out.write(frame)

    # 释放摄像头和视频编码器
    cap.release()
    out.release()

    # 关闭显示窗口
    cv2.destroyAllWindows()

vedio_get = tk.Button(root_window, bg="yellow", fg="black",text="数据采集",width=8, height=3,command=get_vedio(status)).place(relx=0.10, rely=0.6)
vedio_deal = tk.Button(root_window, bg='yellow', fg= 'black', text="实时检测",width=8, height=3).place(relx=0.31, rely=0.6)



root_window.mainloop()
