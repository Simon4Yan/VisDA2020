# encoding: utf-8
"""
@author:  weijian
@contact: dengwj16@gmail.com
"""

import os.path as osp
from .bases import BaseImageDataset


class target_training(BaseImageDataset):
    """
    target_training: only constains camera ID, no class ID information

    Dataset statistics:

    """
    dataset_dir = 'target_training'

    def __init__(self, root='./challenge_datasets', verbose=True, **kwargs):
        super(target_training, self).__init__()
        self.dataset_dir = osp.join(root, self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, 'image_train/')
        self._check_before_run()

        train = self._process_dir(self.train_dir)

        if verbose:
            print("=> Target_training loaded")
            self.print_dataset_statistics(train)

        self.train = train
        self.num_train_pids, self.num_train_imgs, self.num_train_cams = self.get_imagedata_info(self.train)

    def _check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError("'{}' is not available".format(self.dataset_dir))
        if not osp.exists(self.train_dir):
            raise RuntimeError("'{}' is not available".format(self.train_dir))

    def _process_dir(self, dir_path):
        image_list = osp.join(self.dataset_dir, 'label_target_training.txt')
        info = open(image_list).readlines() # image_name, cam_ID, class_ID

        dataset = []
        for i in range(len(info)):
            element = info[i]
            image_name, camid = element.split(' ')[0], element.split(' ')[1]
            pid = 0 # target training has no lables, set ID 0 for all images
            dataset.append((osp.join(dir_path, image_name), pid, int(camid)))
        return dataset
