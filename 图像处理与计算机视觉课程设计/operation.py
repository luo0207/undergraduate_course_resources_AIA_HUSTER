import cv2
import torch
from PIL import Image
from tqdm import tqdm
import numpy as np
import metrics
import glob
from path import *
from utils import save_pre_result

filename = glob.glob(test_src_t1 + '/*.png')


def train(net, dataloader_train, total_step, criterion_ce, optimizer):
    print('Training...')
    model = net.train()
    num = 0
    epoch_loss = 0
    cm_total = np.zeros((2, 2))

    for x1, x2, y in dataloader_train:
        inputs_t1 = x1.to(device)
        inputs_t2 = x2.to(device)
        labels = y.to(device)

        optimizer.zero_grad()
        pre = model(inputs_t1, inputs_t2)
        loss = criterion_ce(pre, labels)   # out_ch=1
        # loss = criterion_ce(pre, torch.squeeze(labels.long(), dim=1))   # out_ch=2
        loss.backward()
        epoch_loss += loss.item()
        optimizer.step()

        # pre = torch.max(pre, 1)[1]  # out_ch=2
        cm = metrics.ConfusionMatrix(2, pre, labels)
        cm_total += cm
        precision, recall, f1, iou, kc = metrics.get_score(cm)

        num += 1

        print('%d/%d, loss:%f, Pre:%f, Rec:%f, F1:%f, IoU:%f, KC:%f' % (num, total_step, loss.item(), precision[1], recall[1], f1[1], iou[1], kc))
    precision_total, recall_total, f1_total, iou_total, kc_total = metrics.get_score_sum(cm_total)

    return epoch_loss, precision_total['precision_1'], recall_total['recall_1'], f1_total['f1_1'], iou_total['iou_1'], kc_total


def validate(net, dataloader_val, epoch):
    print('Validating...')
    model = net.eval()
    num = 0
    cm_total = np.zeros((2, 2))

    for x1, x2, y in tqdm(dataloader_val):
        inputs_t1 = x1.to(device)
        inputs_t2 = x2.to(device)
        labels = y.to(device)
        pre = model(inputs_t1, inputs_t2)
        # pre = torch.max(pre, 1)[1]  # out_ch=2
        cm = metrics.ConfusionMatrix(2, pre, labels)
        cm_total += cm
        num += 1
    precision_total, recall_total, f1_total, iou_total, kc_total = metrics.get_score_sum(cm_total)
    return precision_total['precision_1'], recall_total['recall_1'], f1_total['f1_1'], iou_total['iou_1'], kc_total


def predict(net, dataloader_test,file_list):
    print('Testing...')
    model = net.eval()
    num = 0
    cm_total = np.zeros((2, 2))
    for x1, x2, y in tqdm(dataloader_test):
        inputs_t1 = x1.to(device)
        inputs_t2 = x2.to(device)
        labels = y.to(device)
        pre = model(inputs_t1, inputs_t2)
        cm = metrics.ConfusionMatrix(2, pre, labels)
        data_name=file_list[num]

        cm_total += cm
        save_pre_result(pre, data_name, save_path=test_predict)
        num += 1
    precision_total, recall_total, f1_total, iou_total, kc_total,precision_2,recall_2,f1score_2,iou_2 = metrics.get_score_sum(cm_total)
    return precision_total, recall_total, f1_total, iou_total, kc_total,precision_2,recall_2,f1score_2,iou_2
