# encoding: utf-8
"""
@author:  weijiandeng
@contact: dengwj16@gmail.com
"""

from __future__ import print_function
import sys
sys.path.append(".")
import argparse
import torch
import numpy as np
import torch.nn.functional as F
from learn.model import FT_Resnet
from data.build import make_data_loader_test
from utils.eval_reid import eval_func


def fliplr(img):
    '''flip horizontal'''
    inv_idx = torch.arange(img.size(3)-1,-1,-1).long()  # N x C x H x W
    img_flip = img.index_select(3,inv_idx)
    return img_flip


def test(model, device, test_loader):
    model.eval()
    feature = []
    cams = []
    pids = []
    with torch.no_grad():
        for data, target, cam in test_loader:
            n, c, h, w = data.size()
            ff = torch.FloatTensor(n, 2048).zero_().to(device)
            for i in range(2):
                if (i == 1):
                    data = fliplr(data)
                img = data.to(device)
                outputs = model(img)
                f = outputs
                ff = ff + f
            # norm feature
            fnorm = torch.norm(ff, p=2, dim=1, keepdim=True)
            ff = ff.div(fnorm.expand_as(ff))
            feature.append(ff)
            cams.extend(cam)
            pids.extend(target)

    feature = torch.cat(feature, dim=0).cpu().numpy()
    pids = np.array(pids)
    cams = np.array(cams)
    return feature, pids, cams

def main():
    # Training settings
    parser = argparse.ArgumentParser(description='Test example')
    parser.add_argument('--batch-size', type=int, default=32, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--model_path', type=str, default='./checkpoints/personX/79.pt',
                        help='saved model path')
    args = parser.parse_args()

    use_cuda = not args.no_cuda and torch.cuda.is_available()
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if use_cuda else "cpu")

    query_loader, gallery_loader = make_data_loader_test(batch_size=args.batch_size, dataset='target_validation', use_cuda=use_cuda)

    model_path = args.model_path
    model = FT_Resnet(num_classes=700).to(device)
    model = torch.nn.DataParallel(model)
    try:
        model.load_state_dict(torch.load(model_path)['IDE']) # for espgan
    except:
        model.load_state_dict(torch.load(model_path))

    q_f, q_id, q_cam = test(model, device, query_loader)
    g_f, g_id, g_cam = test(model, device, gallery_loader)

    q_g_dist = np.dot(q_f, np.transpose(g_f))
    q_g_dist = 2. - 2 * q_g_dist  # change the cosine similarity metric to euclidean similarity metric
    all_cmc, mAP = eval_func(q_g_dist, q_id, g_id, q_cam, g_cam)
    all_cmc = all_cmc * 100
    print('rank-1: {:.4f} rank-5: {:.4f} rank-10: {:.4f} rank-20: {:.4f} rank-50: {:.4f} mAP: {:.4f}'.format(all_cmc[0],
                                   all_cmc[4], all_cmc[9], all_cmc[19], all_cmc[49], mAP*100))

    # write txt for challenge server
    # note that mAP is evaluated only on top-100 results
    # indices = np.argsort(q_g_dist, axis=1)
    # np.savetxt("answer.txt", indices[:, :100], fmt="%04d")

if __name__ == '__main__':
    main()
