import torch
import os

# 此处设置CUDA_DEVICE_ID 避免显存不够直接放在cpu上进行测试
# os.environ["CUDA_VISIBLE_ID"] = "2"
# device = torch.device("cuda:2" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")

'''LEVIR-CD'''
dataset_levircd = './LECVD_test'
# train_root = dataset_levircd + '/train'
# train_src_t1 = train_root + '/A'
# train_src_t2 = train_root + '/B'
# train_label = train_root + '/label'

# val_root = dataset_levircd + '/val'
# val_src_t1 = val_root + '/A'
# val_src_t2 = val_root + '/B'
# val_label = val_root + '/label'

test_root = dataset_levircd 
test_src_t1 = test_root + '/A'  # 若测试集的命名格式不同，此处需要修改
test_src_t2 = test_root + '/B'
test_label = test_root + '/label'
test_predict = test_root + '/predict'
os.makedirs(test_predict, exsit_ok=True)


''' DSIFN'''
'''
dataset_dsifn = r'C:/Users/PC/Desktop/DNIST'
train_root = dataset_dsifn + '/train'
train_src_t1 = train_root + '/t1'
train_src_t2 = train_root + '/t2'
train_label = train_root + '/mask_rename'

val_root = dataset_dsifn + '/val'
val_src_t1 = val_root + '/t1'
val_src_t2 = val_root + '/t2'
val_label = val_root + '/mask'

test_root = dataset_dsifn + '/test'
test_src_t1 = test_root + '/t1'
test_src_t2 = test_root + '/t2'
test_label = test_root + '/mask'
test_predict = test_root + '/predict'
'''


''' CDD
dataset_cdd = r'/opt/data/private/Datasets/CDD'
train_root = dataset_cdd + '/train'
train_src_t1 = train_root + '/A'
train_src_t2 = train_root + '/B'
train_label = train_root + '/OUT'

test_root = dataset_cdd + '/test'
test_src_t1 = test_root + '/A'
test_src_t2 = test_root + '/B'
test_label = test_root + '/OUT'
test_predict = test_root + '/predict'

'''