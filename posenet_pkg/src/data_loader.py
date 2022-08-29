import os
import time
import copy
import torch
import torchvision
import pandas as pd
import numpy as np
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models, datasets
import torch.nn.functional as F
import matplotlib.pyplot as plt
from PIL import Image

class CustomDataset(Dataset):
    def __init__(self, image_path, mode, transform, num_val=100):
        self.image_path = image_path
        self.mode = mode
        self.transform = transform

        self.test_filenames = []
        self.test_poses = []
        self.train_filenames = []
        self.train_poses = []
        self.num_train = self.train_filenames.__len__()
        self.num_test = 1

        
    def __getitem__(self,index):
        image = self.image_path
        return self.transform(image)

    def __len__(self):
        if self.mode == 'train':
            num_data = self.num_train
        elif self.mode in ['val', 'test']:
            num_data = self.num_test
        return num_data



def get_loader(model, image_path,mode, batch_size, is_shuffle=False, num_val=100):

    # Predefine image size
    if model == 'Googlenet':
        img_size = 300
        img_crop = 299
    elif model == 'Resnet':
        img_size = 256
        img_crop = 224


    if mode == 'train':
        transform = transforms.Compose([
            transforms.Resize(img_size),
            transforms.RandomCrop(img_crop),
            transforms.ColorJitter(0.5, 0.5, 0.5, 0.2),            
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # metadata_path_val = '/mnt/data2/image_based_localization/posenet/KingsCollege/dataset_test.txt'
        datasets = {'train': CustomDataset(image_path, 'train', transform, num_val),
                    'val': CustomDataset(image_path, 'val', transform, num_val)}
        # data_loaders = {x: DataLoader(datasets[x], batch_size, is_shuffle, num_workers=batch_size)
        #                 for x in ['train', 'val']}
        data_loaders = {'train': DataLoader(datasets['train'], batch_size, is_shuffle, num_workers=4),
                        'val': DataLoader(datasets['val'], batch_size, is_shuffle, num_workers=4)}
    elif mode == 'test':
        transform = transforms.Compose([
            transforms.Resize(img_size),
            transforms.CenterCrop(img_crop),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        batch_size = 1
        is_shuffle = False
        dataset = CustomDataset(image_path, 'test', transform)
        data_loaders = DataLoader(dataset, batch_size, is_shuffle, num_workers=4)

    else:
        assert 'Unavailable Mode'

    return data_loaders

