import torch
import copy
import torch.nn as nn
from torchvision.models import resnet18
from torch.nn.functional import normalize

class PM_Predictor(nn.Module):

    def __init__(self,params, momentum = 0.99):
        """

        :return:
        """
        super().__init__()
        self.model = resnet18(pretrained = True)# pretrained??
        self.model.conv1 = nn.Conv2d(36, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.model.fc = nn.Linear(self.model.fc.in_features,1)

    def forward(self,image):
        """

        :return:
        """
        prediction = self.model(image)
        return prediction

