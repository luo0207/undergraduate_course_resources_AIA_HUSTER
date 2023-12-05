import torch
import torch.utils.data as data
import PIL.Image as Image
import os
import numpy as np


def make_dataset(raw_t1, raw_t2, label, test):
    imgs = []
    file_list = os.listdir(raw_t1)
    #print("file_list_length:",len(file_list))
    #if test:
        #file_list.sort(key=lambda x: int(x[:-4].lstrip('0')))
        #file_list.sort(key=lambda x: int(x[:-4]))
        #print("file_list_length:", file_list)
    for file in file_list:
        img_t1 = os.path.join(raw_t1, file)
        img_t2 = os.path.join(raw_t2, file)
        mask = os.path.join(label, file)
        imgs.append((img_t1, img_t2, mask))
    return imgs,file_list


class RsDataset(data.Dataset):
    def __init__(self, raw_t1, raw_t2, label, test=False, t1_transform=None, t2_transform=None, label_transform=None):
        imgs ,file_list= make_dataset(raw_t1, raw_t2, label, test)
        self.imgs = imgs
        self.t1_transform = t1_transform
        self.t2_transform = t2_transform
        self.label_transform = label_transform
        self.file_list = file_list

    def __getitem__(self, index):
        t1_path, t2_path, y_path = self.imgs[index]
        img_t1 = Image.open(t1_path)
        img_t2 = Image.open(t2_path)
        img_y = Image.open(y_path)

        if self.t1_transform is not None:
            img_t1 = self.t1_transform(img_t1)
        if self.t2_transform is not None:
            img_t2 = self.t2_transform(img_t2)
        if self.label_transform is not None:
            img_y = self.label_transform(img_y)

        return img_t1, img_t2, img_y

    def __len__(self):
        return len(self.imgs)

    def __getfile__(self):
        return self.file_list
