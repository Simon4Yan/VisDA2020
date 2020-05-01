# encoding: utf-8
"""
@author:  weijiandeng
@contact: dengwj16@gmail.com
"""

import torch.nn as nn
from torchvision import models
from torch.nn import functional as F
from torch.nn import init


def weights_init_kaiming(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')
    elif classname.find('Linear') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_out')
        init.constant_(m.bias.data, 0.0)
    elif classname.find('BatchNorm1d') != -1:
        init.normal_(m.weight.data, 1.0, 0.02)
        init.constant_(m.bias.data, 0.0)

def weights_init_classifier(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        init.normal_(m.weight.data, std=0.001)
        init.constant_(m.bias.data, 0.0)

def freeze_bn(modules):
    for m in modules:
        if isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
            m.eval()
            m.weight.requires_grad = False
            m.bias.requires_grad = False

class FT_Resnet(nn.Module):
    def __init__(self, mode='resnet50', num_classes=100, pretrained=True):
        super(FT_Resnet, self).__init__()
        if mode == 'resnet50':
            model = models.resnet50(pretrained=pretrained)
        elif mode == 'resnet101':
            model = models.resnet101(pretrained=pretrained)
        elif mode == 'resnet152':
            model = models.resnet152(pretrained=pretrained)
        else:
            model = models.resnet18(pretrained=pretrained)

        model.layer4[0].conv2.stride = (1,1)
        model.layer4[0].downsample[0].stride = (1,1)

        self.features = nn.Sequential(
            model.conv1,
            model.bn1,
            model.relu,
            model.maxpool,
            model.layer1,
            model.layer2,
            model.layer3,
            model.layer4
        )

        self.num_features = model.layer4[1].conv1.in_channels
        self.feat_bn = nn.BatchNorm1d(self.num_features)
        self.feat_bn.bias.requires_grad_(False)
        init.constant_(self.feat_bn.weight, 1)
        init.constant_(self.feat_bn.bias, 0)

        self.num_classes = num_classes
        self.classifier = nn.Linear(self.num_features, num_classes, bias=False)
        init.normal_(self.classifier.weight, std=0.001)
        self.avg = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        x = self.features(x)
        global_fea = self.avg(x).view(-1, self.num_features)
        fea = self.feat_bn(global_fea)
        output = self.classifier(fea)
        if self.training:
            return global_fea, output
        else:
            fea = F.normalize(fea)
            return fea
