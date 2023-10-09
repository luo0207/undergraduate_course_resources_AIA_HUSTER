import cv2
import face_alignment
import torch
import os
import math
import time
import matplotlib.pyplot as plt

# 关键点检测模型
# Optionally set detector and some additional detector parameters
face_detector = 'sfd'
face_detector_kwargs = {
    "filter_threshold" : 0.8
}
# Run the 3D face alignment on a test image, without CUDA.
fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, device='cuda', flip_input=True,
                                  face_detector=face_detector, face_detector_kwargs=face_detector_kwargs)
threshold = 0.73 # 可根据需求调整
ear_max = 0
# 打开摄像头
cap = cv2.VideoCapture(0)
# 设置帧速率为 30 fps
cap.set(cv2.CAP_PROP_FPS, 30)
# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头,按下q后退出检测")
    exit()
print(cap.get(cv2.CAP_PROP_FPS))
# 获取摄像头的宽度和高度
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
blink_list = [] #记录blink的状态 1眨眼 0未眨眼 2人脸未检测到 3标志点无法检测
ear_list = []
blink_num = 0
frame_num = 0
ear_mean = 0 #不看极大值，极大值会很容易被影响
unblink_num = 0#用于计算ear_mean
t1 = time.time()
print("检测程序开始,按下q键退出眨眼检测程序")
while True:
    # 读取视频帧
    ret, frame = cap.read()
    if ret:
        # 显示当前帧
        blink_flag = 0
        frame_num += 1
        print("第",frame_num,"帧：")
        if (fa.get_landmarks(frame) != None):
            preds = fa.get_landmarks(frame)[-1]
        else:
            blink_flag = 2
            blink_list.append(blink_flag)
            continue
        pl1, pl2, pl3, pl4, pl5, pl6, pr1, pr2, pr3, pr4, pr5, pr6 = preds[36:48, :]
        l14, r14 = math.dist(pl1, pl4), math.dist(pr1, pr4)
        if (r14 < 1e-5 and l14 > 1e-5):  # 避免除0
            r14 = l14
        elif (l14 < 1e-5 and r14 > 1e-5):
            l14 = r14
        elif (l14 < 1e-5 and r14 < 1e-5):
            r14, l14 = 1.0, 1.0
        l26_cur, l35_cur, r26_cur, r35_cur = math.dist(pl2, pl6), math.dist(pl3, pl5), math.dist(pr2,pr6), math.dist(pr3, pr5)
        lear_cur = (l26_cur + l35_cur) / (2 * l14)
        rear_cur = (r26_cur + r35_cur) / (2 * r14)
        ear_cur = (lear_cur + rear_cur) / 2
        if(ear_cur>0.5):
            continue #异常检测
        ear_list.append(ear_cur)
        if(ear_cur<0.73*ear_mean and blink_list[-1]!=1): #上一帧不能闭眼
            print("blink-detected!")
            blink_num += 1
            blink_flag = 1
        else:
            ear_mean = (ear_mean*unblink_num +ear_cur)/(unblink_num+1)
            unblink_num += 1
            blink_flag = 0
        blink_list.append(blink_flag)
        print("EAR_Mean:",ear_mean, "EAR_CUR", ear_cur)
        if(blink_flag==1):
            cv2.putText(frame,"blink",(int(0.7*width),int(0.2*height)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0), 1)
        #可视化
        for i in range(36,48):
            cv2.circle(frame, (int(preds[i][0]), int(preds[i][1])), 1, (255, 0, 0), 1)
        cv2.imshow('Frame', frame)
    # 检查是否按下了 'q' 键，如果是则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头和视频编码器
t2 = time.time()
cap.release()
# 关闭显示窗口
cv2.destroyAllWindows()
freq = int(blink_num/((t2-t1)/60))
print("检测时长为{}分钟".format((t2-t1)/60))
print("总共眨眼次数为:",blink_num,"眨眼频率为{}次/分钟".format(freq))

plt.figure(1)
plt.plot(range(len(ear_list)), ear_list)
plt.xlabel('frame index')
plt.ylabel('EAR')
plt.title("EAR-frame")
plt.show()