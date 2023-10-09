import face_alignment
import math
from skimage import io
import numpy as np
import os
import time

# Optionally set detector and some additional detector parameters
face_detector = 'sfd'
face_detector_kwargs = {
    "filter_threshold" : 0.8
}

# Run the 3D face alignment on a test image, without CUDA.
fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, device='cuda', flip_input=True,
                                  face_detector=face_detector, face_detector_kwargs=face_detector_kwargs)

threshold = 0.62 #较优threshold 0.73 用于测试
def blink(path, blink_num, threshold = 0.6):
    print("blink")
    path = path
    blink_num = blink_num
    TP, FP, TN, FN = 0,0,0,0
    ear = np.zeros((blink_num, 13))
    blink = np.zeros((blink_num,13), dtype=int)
    for i in range(0, blink_num):
        l26_max, l35_max, r26_max, r35_max = 0, 0, 0, 0
        r14, l14 = 50, 50
        lear_max, rear_max, ear_max, lear_cur, rear_cur, ear_cur = 0, 0, 0, 0, 0, 0
        l14_avg, r14_avg = 0, 0
        for j in range(0,13):
            blink_flag = 3  # 2代表缺图 1代表眨眼 0代表没眨眼 3代表检测失败
            path_cur = os.path.join(path, str(i + 1), str(j + 1))
            path_cur += ".png"
            if os.path.exists(path_cur):
                img = io.imread(path_cur)
            else:
                blink_flag = 2  # 无照片
                blink[i, j] = blink_flag
                ear[i, j] = max(ear[i, :])
                continue
            # print(j)
            if(fa.get_landmarks(img)!=None): #防止没被检测到
                preds = fa.get_landmarks(img)[-1]
            else:
                blink_flag = 3  # 无照片
                blink[i, j] = blink_flag
                ear[i, j] = max(ear[i, :])
                continue
            pl1, pl2, pl3, pl4, pl5, pl6, pr1, pr2, pr3, pr4, pr5, pr6 = preds[36:48, :]
            l14, r14 = math.dist(pl1, pl4), math.dist(pr1, pr4)
            if (r14 < 1e-5 and l14 > 1e-5): #避免除0
                r14 = l14
            elif (l14 < 1e-5 and r14 > 1e-5):
                l14 = r14
            elif (l14 < 1e-5 and r14 < 1e-5):
                r14, l14 = 1.0, 1.0
            l14_avg, r14_avg = (l14_avg * (j) + l14) / (j + 1), (r14_avg * (j) + r14) / (j + 1)  # 求r14 和 l14的平均 来算earmax
            if(l14_avg< 1e-5): l14_avg =1.0
            if(r14_avg<1e-5) :r14_avg =1.0
            l26_cur, l35_cur, r26_cur, r35_cur = math.dist(pl2, pl6), math.dist(pl3, pl5), math.dist(pr2,pr6), math.dist(pr3, pr5)
            if (l26_cur > l26_max): l26_max = l26_cur
            if (l35_cur > l35_max): l35_max = l35_cur
            if (r35_cur > r35_max): r35_max = r35_cur
            if (r26_cur > r26_max): r26_max = r26_cur
            lear_cur = (l26_cur + l35_cur) / (2 * l14)
            rear_cur = (r26_cur + r35_cur) / (2 * r14)
            ear_cur = (lear_cur + rear_cur) / 2
            lear_max = (l26_max + l35_max) / (2 * l14_avg)
            rear_max = (r26_max + r35_max) / (2 * r14_avg)
            ear_max = (lear_max + rear_max) / 2.0
            ear[i, j] = ear_cur
            if (ear_cur < threshold * ear_max):
                blink_flag = 1
            else:
                blink_flag = 0
            blink[i, j] = blink_flag
        print("第{}个片段：blink {}, ear{} ,ear_max:{}".format(i + 1, blink[i], ear[i], ear_max))
        np.save('test_blink_blink_'+str(threshold), blink)
        np.save("test_blink_ear_"+str(threshold), ear)

    for i in range(blink_num):
        if(1 in blink[i,:] or (min(ear[i, :]) < threshold * max(ear[i, :]))):TP += 1
        else:
            FN += 1
    return TP, FN

def unblink(path, blink_num,threshold=0.6):
    print("unblink")
    path = path
    blink_num = blink_num
    TP, FP, TN, FN = 0, 0, 0, 0
    ear = np.zeros((blink_num, 13))
    blink = np.zeros((blink_num, 13), dtype=int)
    for i in range(0, blink_num):
        l26_max, l35_max, r26_max, r35_max = 0, 0, 0, 0
        r14, l14 = 50, 50
        lear_max, rear_max, ear_max, lear_cur, rear_cur, ear_cur = 0, 0, 0, 0, 0, 0
        l14_avg, r14_avg = 0, 0
        for j in range(13):
            blink_flag = 3  # 2代表检测失败 1代表眨眼 0代表没眨眼
            path_cur = os.path.join(path, str(i + 1), str(j + 1))
            path_cur += ".png"
            if os.path.exists(path_cur):
                img = io.imread(path_cur)
            else:
                blink_flag = 2 #无照片
                blink[i, j] = blink_flag
                ear[i, j] = max(ear[i,:])
                continue
            if (fa.get_landmarks(img) != None):  # 防止没被检测到
                preds = fa.get_landmarks(img)[-1]
            else:
                blink_flag = 3  # 无照片
                blink[i, j] = blink_flag
                ear[i, j] = max(ear[i, :])
                continue
            pl1, pl2, pl3, pl4, pl5, pl6, pr1, pr2, pr3, pr4, pr5, pr6 = preds[36:48, :]
            l14, r14 = math.dist(pl1, pl4), math.dist(pr1, pr4)
            if (r14 < 1e-5 and l14 > 1e-5):  # 避免除0
                r14 = l14
            elif (l14 < 1e-5 and r14 > 1e-5):
                l14 = r14
            elif (l14 < 1e-5 and r14 < 1e-5):
                r14, l14 = 1.0, 1.0
            l14_avg, r14_avg = (l14_avg * (j) + l14) / (j + 1), (r14_avg * (j) + r14) / (j + 1)  # 求r14 和 l14的平均 来算earmax
            if (l14_avg < 1e-5): l14_avg = 1.0
            if (r14_avg < 1e-5): r14_avg = 1.0
            l26_cur, l35_cur, r26_cur, r35_cur = math.dist(pl2, pl6), math.dist(pl3, pl5), math.dist(pr2,pr6), math.dist(pr3, pr5)
            if (l26_cur > l26_max): l26_max = l26_cur
            if (l35_cur > l35_max): l35_max = l35_cur
            if (r35_cur > r35_max): r35_max = r35_cur
            if (r26_cur > r26_max): r26_max = r26_cur
            lear_cur = (l26_cur + l35_cur) / (2 * l14)
            rear_cur = (r26_cur + r35_cur) / (2 * r14)
            ear_cur = (lear_cur + rear_cur) / 2
            lear_max = (l26_max + l35_max) / (2 * l14_avg)
            rear_max = (r26_max + r35_max) / (2 * r14_avg)
            ear_max = (lear_max + rear_max) / 2.0
            ear[i, j] = ear_cur
            if (ear_cur < threshold * ear_max):
                blink_flag = 1
            else:
                blink_flag = 0
            blink[i, j] = blink_flag
        print("第{}个片段：unblink {}, ear{} ,ear_max:{}".format(i + 1, blink[i], ear[i], ear_max))
        np.save('test_unblink_blink_'+str(threshold), blink)
        np.save("test_unblink_ear_"+str(threshold), ear)
    for i in range(blink_num):
        if (1 in blink[i, :] or (min(ear[i, :]) < threshold * max(ear[i, :]))):
            FP += 1
        else:
            TN += 1
    return FP, TN

# TP, FN = blink(threshold=threshold)
# FP, TN = unblink(threshold=threshold)
#test
t1 = time.time()
TP, FN = blink(threshold = threshold, path = "D:\\file\\3rd_down\\eye_blink\\data_my\\blink\\all", blink_num=635)
FP, TN = unblink(threshold = threshold, path = "D:\\file\\3rd_down\\eye_blink\\data_my\\unblink\\all", blink_num=1054)
t2 = time.time()
print("TP:{}, FN{}, FP:{}, TN{}".format(TP, FN,FP, TN))
Recall = TP/(TP + FN)
Precession = TP/(TP + FP)
F1 = 2*Recall*Precession/(Recall + Precession)

print("Precision:{}, Recall:{}, F1:{}".format(Precession, Recall, F1))
FMiss = 0
FMiss_pic = 0
blink = np.load("test_blink_blink_" +str(threshold)+".npy")
for i in range(127):
    if (3 in blink[i, :] ):
        FMiss +=1
FMiss_pic += len(np.where(3==blink)[0])

blink = np.load("test_unblink_blink_"+ str(threshold)+".npy")
for i in range(98):
    if (3 in blink[i, :]):
        FMiss += 1
FMiss_pic += len(np.where(3==blink)[0])
print("Fmiss:{}, Fmissrate:{}, Fmiss_pic:{}, Fmiss_pic_rate:{}".format(FMiss, FMiss/(127+98),FMiss_pic, FMiss_pic/((127+98)*13)))

print("总运行时间:{}s, 每一帧运行时间:{}s, 一分钟可以处理的帧数:{} frames".format((t2-t1), (t2-t1)/((127+98)*13), 60/((t2-t1)/((127+98)*13))))




















    # 获取第一个和第二个点的坐标（相对于图片而不是框出来的人脸）
    # print("Part 0: {}, Part 1: {} ...".format(shape.part(0), shape.part(1)))

    # 绘制特征点
    # for index, pt in enumerate(shape.parts()):
    #     print('Part {}: {}'.format(index, pt))
    #     pt_pos = (pt.x, pt.y)
    #     cv2.circle(img, pt_pos, 1, (255, 0, 0), 2)
    #     # 利用cv2.putText输出1-68
    #     font = cv2.FONT_HERSHEY_SIMPLEX
    #     cv2.putText(img, str(index + 1), pt_pos, font, 0.3, (0, 0, 255), 1, cv2.LINE_AA)

# cv2.imshow('img', img)
# k = cv2.waitKey()
# cv2.destroyAllWindows()