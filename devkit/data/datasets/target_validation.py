# encoding: utf-8
"""
@author:  weijian
@contact: dengwj16@gmail.com
"""

from __future__ import print_function
import sys
sys.path.append("..")
import glob
import re
import os.path as osp

from .bases import BaseImageDataset


class target_validation(BaseImageDataset):
    """
    personX (source domain): only consains training samples
    Dataset statistics:
    # query_identities: 100
    # query_images: 377
    # gallery_images: 2944
    # cams: 5
    """

    dataset_dir = 'target_validation'

    def __init__(self, root='./challenge_datasets', verbose=True):
        super(target_validation, self).__init__()
        self.dataset_dir = osp.join(root, self.dataset_dir)
        self.query_dir = osp.join(self.dataset_dir, 'image_query/')
        self.gallery_dir = osp.join(self.dataset_dir, 'image_gallery/')
        self._check_before_run()
        self.query = self._process_dir(self.query_dir, relabel=False)
        self.gallery = self._process_dir(self.gallery_dir, relabel=False)
        if verbose:
            print("=> target_validation loaded")
            self.print_dataset_statistics_validation(self.query, self.gallery)

    def _check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError("'{}' is not available".format(self.dataset_dir))
        if not osp.exists(self.query_dir):
            raise RuntimeError("'{}' is not available".format(self.query_dir))
        if not osp.exists(self.gallery_dir):
            raise RuntimeError("'{}' is not available".format(self.gallery_dir))

    def _process_dir(self, dir_path, relabel=False):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
        pattern = re.compile(r'([-\d]+)_c(\d)')

        pid_container = set()
        for img_path in img_paths:
            pid, _ = map(int, pattern.search(img_path).groups())
            if pid == -1: continue  # junk images are just ignored
            pid_container.add(pid)
        pid2label = {pid: label for label, pid in enumerate(pid_container)}

        dataset = []
        for img_path in img_paths:
            pid, camid = map(int, pattern.search(img_path).groups())
            if pid == -1: continue  # junk images are just ignored
            assert 0 <= pid <= 100  # pid == 0 means background
            assert 1 <= camid <= 6 # num_camid=5, max_cam_index=6
            camid -= 1  # index starts from 0
            if relabel: pid = pid2label[pid]
            dataset.append((img_path, pid, camid))

        return dataset
