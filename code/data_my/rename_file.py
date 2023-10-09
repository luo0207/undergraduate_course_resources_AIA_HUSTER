import os

path = "D:/file/3rd_down/eye_blink/data_my/Labeled/unblink/watch_video"

file_lists = os.listdir(path)
begin_num = 840
for i in range(len(file_lists)):
    src = os.path.join(path, str(file_lists[i]))
    if(os.path.exists(src)):
        dst = os.path.join(path,str(i+1+begin_num))
        os.rename(src=src, dst=dst)
    else:
        pass