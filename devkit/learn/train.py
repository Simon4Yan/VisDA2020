# encoding: utf-8
"""
@author:  weijiandeng
@contact: dengwj16@gmail.com
"""

from __future__ import print_function
import sys
sys.path.append(".")
import os
import argparse
import torch
from tqdm import trange
import torch.nn.functional as F
from learn.model import FT_Resnet
from learn.loss import TripletLoss, CrossEntropyLabelSmooth
from utils.utils import WarmupMultiStepLR
from data.build import make_data_loader
from data import IterLoader


tri_criteria= TripletLoss(margin=0.5)
cls_criteria = CrossEntropyLabelSmooth(num_classes=700)
def train(args, model, device, train_loader, optimizer, epoch):
    model.train()
    for i in range(args.iters):
        data, target = train_loader.next()
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        feature, output = model(data)
        loss_ce = cls_criteria(output, target)
        loss_tri = tri_criteria(feature, target)
        loss = loss_ce + loss_tri
        loss.backward()
        optimizer.step()

        if i % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\t \t CE Loss: {:.6f} Tir Loss: {:.6f}'.format(
                epoch, i + 1, args.iters,
                100. * i + 1 / args.iters, loss_ce.item(), loss_tri.item()))

def main():
    # Training settings
    parser = argparse.ArgumentParser(description='Train with cross-entropy loss')
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--epochs', type=int, default=60, metavar='N',
                        help='number of epochs to learn (default: 14)')
    parser.add_argument('--iters', type=int, default=150)
    parser.add_argument('--lr', type=float, default=0.00035, metavar='LR',
                        help='learning rate (default: 0.00035)')
    parser.add_argument('--gamma', type=float, default=0.1, metavar='M',
                        help='Learning rate step gamma (default: 0.7)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--weight-decay', type=float, default=5e-4)
    parser.add_argument('--save-model', action='store_true', default=True,
                        help='For Saving the current Model')
    args = parser.parse_args()

    use_cuda = not args.no_cuda and torch.cuda.is_available()
    if args.seed is not None:
        torch.manual_seed(args.seed)
    device = torch.device("cuda" if use_cuda else "cpu")

    source_loader = IterLoader(make_data_loader(batch_size=args.batch_size, dataset='personX_spgan', use_cuda=use_cuda, tri_sample=True))

    model = FT_Resnet(num_classes=700)
    model = model.to(device)
    model = torch.nn.DataParallel(model)
    params = []
    for key, value in model.named_parameters():
        if not value.requires_grad:
            continue
        params += [{"params": [value], "lr": args.lr, "weight_decay": args.weight_decay}]
    optimizer = torch.optim.Adam(params)
    scheduler = WarmupMultiStepLR(optimizer, milestones=[30, 50], gamma=0.1, warmup_factor=0.01,
                                     warmup_iters=10)

    for epoch in trange(args.epochs):
        source_loader.new_epoch()
        train(args, model, device, source_loader, optimizer, epoch)
        scheduler.step()
        if args.save_model and (epoch+1) % 10 == 0:
            save_rb_path = './checkpoints/personX/'
            if not os.path.exists(save_rb_path):
                os.makedirs(save_rb_path)
            torch.save(model.state_dict(), save_rb_path + str(epoch) + '.pt')

if __name__ == '__main__':
    main()
