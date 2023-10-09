import os
import cv2
import face_alignment
import pandas as pd
import math
import time


# 关键点检测模型
# Optionally set detector and some additional detector parameters
face_detector = 'sfd'
face_detector_kwargs = {
    "filter_threshold" : 0.8
}
# Run the 3D face alignment on a test image, without CUDA.
fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, device='cuda:0', flip_input=True,
                                  face_detector=face_detector, face_detector_kwargs=face_detector_kwargs)
result = pd.DataFrame()
threshold = 0.70 # 可根据需求调整
def blink_count(path, count):
    # 打开摄像头
    cap = cv2.VideoCapture(path)
    # 设置帧速率为 30 fps
    cap.set(cv2.CAP_PROP_FPS, 30)
    save_path = os.path.join("D:\\file\\3rd_down\\eye_blink\\HUST-LBEW\\untrimmed-video",str(count))+".avi"
    # 获取摄像头的宽度和高度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # 创建视频编码器，用于保存视频
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(save_path, fourcc, 30.0, (width, height))
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开视频")
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
    while True:
        # 读取视频帧
        ret, frame = cap.read()
        if ret:
            # 显示当前帧
            blink_flag = 0
            frame_num += 1
            # print("第",frame_num,"帧：")
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
            if(ear_cur<threshold*ear_mean and blink_list[-1]!=1): #上一帧不能闭眼
                # print("blink-detected!")
                blink_num += 1
                blink_flag = 1
            else:
                ear_mean = (ear_mean*unblink_num +ear_cur)/(unblink_num+1)
                unblink_num += 1
                blink_flag = 0
            blink_list.append(blink_flag)
            print("EAR_Mean:",ear_mean, "EAR_CUR", ear_cur)
            if(blink_flag==1):
                cv2.putText(frame,"blink",(int(0.7*width),int(0.2*height)),cv2.FONT_HERSHEY_SIMPLEX,2,(255, 0, 255), 2)
            for i in range(36,48):
                cv2.circle(frame, (int(preds[i][0]), int(preds[i][1])), 1, (255, 255, 0), 1)
            cv2.rectangle(frame, (int(preds[36][0]-15), int(preds[37][1]-15)), (int(preds[39][0]+15), int(preds[40][1]+15)), (255, 255, 0),1)
            cv2.rectangle(frame, (int(preds[42][0]-15), int(preds[43][1]-15)), (int(preds[45][0]+15), int(preds[46][1]+15)), (255, 255, 0),1)

            cv2.imshow('Frame', frame)
            # 保存当前帧到视频文件
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # 释放摄像头和视频编码器
    cap.release()
    out.release()
    # 关闭显示窗口
    cv2.destroyAllWindows()
    freq = int(blink_num/((frame_num)/(30*60)))
    print("检测时长为{}分钟".format(((frame_num)/(30*60))))
    print("总共眨眼次数为:",blink_num,"眨眼频率为{}次/分钟".format(freq))
    return freq

# path = "D:/file/3rd_down/eye_blink/avi/play game"
play_game_list = []
watch_video_list = []
write_code_list = []
read_paper_list = []
# path = "D:/file/3rd_down/eye_blink/avi"
path = "./avi"
# path = "D:\\file\\3rd_down\\eye_blink\\HUST-LBEW\\untrimmed-video\\longvideo"
count = 0
for file, sub_file, videos in os.walk(path):
     for video in videos:
         count += 1
         video_path = os.path.join(file, video)
         freq = blink_count(video_path, count)
         print("处理的视频为：", video_path, "眨眼频率为:", freq)
#          if("game" in video_path):
#             play_game_list.append(freq)
#          elif("watch" in video_path):
#              watch_video_list.append(freq)
#          elif("code" in video_path):
#              write_code_list.append(freq)
#          elif("paper" in video_path):
#              read_paper_list.append(freq)
# result['play_game'] = pd.Series(play_game_list)
# result['watch_video'] = pd.Series(watch_video_list)
# result['write_code'] = pd.Series(write_code_list)
# result['read_paper'] = pd.Series(read_paper_list)
#
# print(result)
# result.to_csv('result.csv')
