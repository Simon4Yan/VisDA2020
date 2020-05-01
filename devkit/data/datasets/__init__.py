# encoding: utf-8
"""
@author:  weijiandeng
@contact: dengwj16@gmail.com
"""

from .personX import personX
from .personX_spgan import personX_spgan
from .target_validation import target_validation
from .target_training import target_training
from .dataset_loader import ImageDataset

__factory = {
    'personX': personX,
    'personX_spgan': personX_spgan,
    'target_validation': target_validation,
    'target_training': target_training,
}


def get_names():
    return __factory.keys()


def init_dataset(name, *args, **kwargs):
    if name not in __factory.keys():
        raise KeyError("Unknown datasets: {}".format(name))
    return __factory[name](*args, **kwargs)
