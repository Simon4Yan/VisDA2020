# encoding: utf-8
"""
@author:  weijian
@contact: dengwj16@gmail.com
"""

import torchvision.transforms as T


def build_transforms(before_size = [256, 128], input_size = [256, 128], mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225], is_train=True, is_colorjitter=False):
    normalize_transform = T.Normalize(mean=mean, std=std)
    if is_train:
        transform = T.Compose([
            T.Resize(before_size, interpolation=3),
            T.RandomHorizontalFlip(),
            T.Pad(10),
            T.RandomCrop(input_size),
            T.ToTensor(),
            normalize_transform
        ])

    elif is_train and is_colorjitter:
        transform = T.Compose([
            T.Resize(before_size, interpolation=3),
            T.RandomHorizontalFlip(),
            T.Pad(10),
            T.RandomCrop(input_size),
            T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0),# light
            T.ToTensor(),
            normalize_transform
        ])
    else:
        transform = T.Compose([
            T.Resize(input_size, interpolation=3),
            T.ToTensor(),
            normalize_transform
        ])

    return transform
