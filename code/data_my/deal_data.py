import os
import cv2
import matplotlib.pyplot as plt
path = "D:/file/3rd_down/eye_blink/data_my" #只需要更改文件根目录
# 先罗列出所有需要处理的数据集
video_pathlist = []
for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if(filename.endswith(".avi")):
            video_pathlist.append(os.path.join(dirpath, filename))
print(video_pathlist)
for video_path in video_pathlist:
    # if("game" in video_path):
    #     state = "play_game"
    # elif("paper" in video_path):
    #     state = "read_paper"
    # elif("watch" in video_path):
    #     state = "watch_video"
    # elif("code" in video_path):
    #     state = "write_code"
    print("现在处理的的视频地址为:", video_path)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("位于{}视频打开失败".format(video_path))
        continue
    count = 0 #13个为一组的计数器
    while True:
        if(count==0):
            img_list = []
        ret, img = cap.read()
        if ret:
            img_list.append(img)
            count += 1
            cv2.imwrite(str(count + 1) + ".png", img)
        else:
            break

        # if(count == 13): #开始显示并标注是睁眼还是闭眼
        #     for i in range(13):
        #         cv2.imshow("img" +str(i+1),img_list[i])
        #         cv2.waitKey(150)
        #         cv2.destroyAllWindows()
        #     blink_flag = input("请输入这十三帧是否闭眼，0睁眼,1闭眼,其余0则是这13帧不作为数据：")
        #
        #     if (blink_flag == "1"): blink_type = "blink"
        #     elif(blink_flag =="0"): blink_type = "unblink"
        #     else:
        #         count =0
        #         continue
        #     #保存
        #     save_path = os.path.join(path, blink_type, state)
        #     all_file = os.listdir(save_path)
        #     idx = len(all_file) + 1
        #     for i in range(13):#按照文件夹保存文件
        #         frame_path = os.path.join(save_path, str(idx))
        #         if not os.path.exists(frame_path):
        #             os.makedirs(frame_path)
        #             os.chdir(frame_path)
        #         cv2.imwrite(str(i+1)+".png", img_list[i])
        #     count = 0

    cap.release()