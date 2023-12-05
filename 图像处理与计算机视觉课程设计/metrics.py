import torch
import numpy as np
from sklearn.metrics import confusion_matrix



def ConfusionMatrix(num_classes, pres, gts):
    def __get_hist(pre, gt):
        pre = pre.cpu().detach().numpy()
        gt = gt.cpu().detach().numpy()
        pre[pre >= 0.5] = 1
        pre[pre < 0.5] = 0
        gt[gt >= 0.5] = 1
        gt[gt < 0.5] = 0
        mask = (gt >= 0) & (gt < num_classes)
        label = num_classes * gt[mask].astype(int) + pre[mask].astype(int)
        hist = np.bincount(label, minlength=num_classes ** 2).reshape(num_classes, num_classes)
        return hist

    cm = np.zeros((num_classes, num_classes))
    for lt, lp in zip(gts, pres):
        cm += __get_hist(lt.flatten(), lp.flatten())
    return cm


def get_score(confusionMatrix):
    precision_2=confusionMatrix[1][1] / (confusionMatrix[1][1] +confusionMatrix[1][0] + np.finfo(np.float32).eps)
    recall_2=confusionMatrix[1][1] / (confusionMatrix[1][1] +confusionMatrix[0][1] + np.finfo(np.float32).eps)
    f1score_2 = 2 * precision_2 * recall_2 / ((precision_2 + recall_2) + np.finfo(np.float32).eps)
    iou_2=confusionMatrix[1][1] / (confusionMatrix[1][1] +confusionMatrix[1][0]+confusionMatrix[0][1] + np.finfo(np.float32).eps)
    precision = np.diag(confusionMatrix) / (confusionMatrix.sum(axis=0) + np.finfo(np.float32).eps)
    recall = np.diag(confusionMatrix) / (confusionMatrix.sum(axis=1) + np.finfo(np.float32).eps)
    f1score = 2 * precision * recall / ((precision + recall) + np.finfo(np.float32).eps)
    iou = np.diag(confusionMatrix) / (
            confusionMatrix.sum(axis=1) + confusionMatrix.sum(axis=0) - np.diag(confusionMatrix) + np.finfo(
        np.float32).eps)
    po = np.diag(confusionMatrix).sum() / (confusionMatrix.sum() + np.finfo(np.float32).eps)
    pe = (confusionMatrix[0].sum() * confusionMatrix[0:2][0].sum() + confusionMatrix[1].sum() * confusionMatrix[0:2][
        1].sum()) / confusionMatrix.sum() ** 2 + np.finfo(np.float32).eps
    kc = (po - pe) / (1 - pe + np.finfo(np.float32).eps)
    return precision, recall, f1score, iou, kc,precision_2,recall_2,f1score_2,iou_2


def get_score_sum(confusionMatrix):
    num_classes = confusionMatrix.shape[0]
    precision, recall, f1score, iou, kc,precision_2,recall_2,f1score_2,iou_2 = get_score(confusionMatrix)
    cls_precision = dict(zip(['precision_' + str(i) for i in range(num_classes)], precision))
    cls_recall = dict(zip(['recall_' + str(i) for i in range(num_classes)], recall))
    cls_f1 = dict(zip(['f1_' + str(i) for i in range(num_classes)], f1score))
    cls_iou = dict(zip(['iou_' + str(i) for i in range(num_classes)], iou))
    return cls_precision, cls_recall, cls_f1, cls_iou, kc,precision_2,recall_2,f1score_2,iou_2
