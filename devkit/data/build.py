# encoding: utf-8
"""
@author:  weijiandeng
@contact: dengwj16@gmail.com
"""

from torch.utils.data import DataLoader

from .collate_batch import train_collate_fn, val_collate_fn
from .datasets import init_dataset, ImageDataset
from .transforms import build_transforms
from .samplers import RandomMultipleGallerySampler


def make_data_loader(batch_size=16, dataset='personX', use_cuda=False, is_train=True, tri_sample=False):
    train_transforms = build_transforms(is_train=is_train)
    dataset = init_dataset(dataset)

    train_set = ImageDataset(dataset.train, train_transforms)
    kwargs = {'num_workers': 4, 'pin_memory': True} if use_cuda else {}

    if tri_sample:
        train_loader = DataLoader(
            train_set, batch_size=batch_size,
            sampler=RandomMultipleGallerySampler(dataset.train, num_instances=4),
            collate_fn=train_collate_fn, drop_last=True, shuffle=False, **kwargs
        )

    else:
        train_loader = DataLoader(
            train_set, batch_size=batch_size, shuffle=False, drop_last=True,
            collate_fn=train_collate_fn, **kwargs
        )

    return train_loader

def make_data_loader_test(batch_size=32, dataset='target_validation', use_cuda=False, shuffle=False):
    test_transforms = build_transforms(is_train=False)
    dataset = init_dataset(dataset)

    query_set = ImageDataset(dataset.query, test_transforms)
    gallery_set = ImageDataset(dataset.gallery, test_transforms)
    kwargs = {'num_workers': 4, 'pin_memory': True} if use_cuda else {}
    query_loader = DataLoader(
        query_set, batch_size=batch_size, shuffle=shuffle,
        collate_fn=val_collate_fn, **kwargs
    )
    gallery_loader = DataLoader(
        gallery_set, batch_size=batch_size, shuffle=shuffle,
        collate_fn=val_collate_fn, **kwargs
    )

    return query_loader, gallery_loader
