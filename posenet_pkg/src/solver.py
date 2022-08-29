import sys
sys.path.append("/home/ydh/posenet_pkg/posenet_pkg/posenet_pkg")
import os
import time
import numpy as np
import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.optim import lr_scheduler
from tensorboardX import SummaryWriter
from model import model_parser
from model import PoseLoss
from PIL import Image
from pose_utils import *
from data_loader import get_loader

class Solver():
    def __init__(self, data_loader):
        self.data_loader = data_loader

        # do not use dropout if not bayesian mode
        # if not self.config.bayesian:
        #     self.config.dropout_rate = 0.0

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.model = model_parser(model='Resnet', fixed_weight=False, dropout_rate=0.5,
                                  bayesian=False)

    def test(self):
        global pos_out
        global ori_out

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.model = self.model.to(self.device)
        self.model.eval()

        test_model_path = '/home/ydh/catkin_ws/src/rosbag_pkg/src/model/199_net.pth'

        self.model.load_state_dict(torch.load(test_model_path))

        for i, inputs in enumerate(self.data_loader):
            inputs = inputs.to(self.device)
            pos_out, ori_out, _ = self.model(inputs)
            pos_out = pos_out.squeeze(0).detach().cpu().numpy()
            ori_out = F.normalize(ori_out, p=2, dim=1)
            ori_out = quat_to_euler(ori_out.squeeze(0).detach().cpu().numpy())
            
        return pos_out, ori_out
