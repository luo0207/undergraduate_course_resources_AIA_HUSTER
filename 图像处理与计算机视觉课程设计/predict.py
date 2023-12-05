from collections import OrderedDict
import numpy as np
import os
from torch.utils.data import DataLoader
from torchvision import transforms
from operation import predict
from path import *
import torch
from dataset import RsDataset
from networks.USSFCNet import USSFCNet
from thop import profile


src_transform = transforms.Compose([
    transforms.ToTensor(),
    # transforms.Resize(512),
    transforms.Normalize([0.5], [0.5])
])

label_transform = transforms.Compose([
    transforms.ToTensor(),
    # transforms.Resize(512),
])
def count_param(model):
    param_count = 0
    for param in model.parameters():
        param_count += param.view(-1).size()[0]
    return param_count

model = USSFCNet(3, 1, ratio=0.5).to(device)
# model = torch.nn.DataParallel(model, device_ids=device_ids).to(device)
model_path = './ckps/USSFCNet_LEVIRCD/ckp_f1_9110.pth'
ckps = torch.load(model_path, map_location=device)
model.load_state_dict(ckps)
p_count = count_param(model)
print('params:', p_count)
input = torch.randn(1, 3, 1024, 1024).to(device)
flops, params = profile(model, inputs=(input, input,))
file_list=[]
print('flops:', flops, ' params:', params)
dataset_test = RsDataset(test_src_t1, test_src_t2, test_label, test=True,
                         t1_transform=src_transform,
                         t2_transform=src_transform,
                         label_transform=label_transform)
file_list=dataset_test.__getfile__()

dataloader_test = DataLoader(dataset_test,
                             batch_size=1,
                             shuffle=False)
pre_test, rec_test, f1_test, iou_test, kc_test,precision_2,recall_2,f1score_2,iou_2 = predict(model, dataloader_test,file_list)
print('test Pre:(%f,%f) test Recall:(%f,%f) test MeanF1Score:(%f,%f) test IoU:(%f,%f) test KC: %f' % (
    pre_test['precision_0'], pre_test['precision_1'], rec_test['recall_0'], rec_test['recall_1'], f1_test['f1_0'],
    f1_test['f1_1'], iou_test['iou_0'], iou_test['iou_1'], kc_test))
print("precision",precision_2,"recall",recall_2,"f1score",f1score_2,"iou",iou_2)
