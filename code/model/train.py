import argparse

import torch.utils.data
from torchvision.models import resnet18
from pm_images_dataset import PM_Images_Dataset
import torch.optim as optim
from pm_predictor import PM_Predictor
from torch.utils.data import random_split
from torch.utils.data import DataLoader
from torch.nn import MSELoss
import tqdm
import sys
import os
import time
import pydevd_pycharm
pydevd_pycharm.settrace('132.69.242.121', port=51117, stdoutToServer=True, stderrToServer=True)

import torchvision.transforms as T
# parser = argparse.ArgumentParser()
#
#
# parser.add_argument('--gpu', type=int, default=1, help='GPU to use [default: GPU 0]')5
# parser.add_argument('--batch', type=int, default=32, help='Batch Size during training [default: 32]')
# parser.add_argument('--epoch', type=int, default=200, help='Epoch to run [default: 50]')
# parser.add_argument('--output_dir', type=str, default='train_results', help='Directory that stores all training logs and trained models')
# parser.add_argument('--wd', type=float, default=0, help='Weight Decay [Default: 0.0]')
# FLAGS = parser.parse_args()
# parser = argparse.ArgumentParser()
# parser.add_argument("--dataset_path", type=str, default="data/UCF-101-frames", help="Path to UCF-101 dataset")
# parser.add_argument("--split_path", type=str, default="data/ucfTrainTestlist", help="Path to train/test split")
# parser.add_argument("--split_number", type=int, default=1, help="train/test split number. One of {1, 2, 3}")
# parser.add_argument("--num_epochs", type=int, default=100, help="Number of training epochs")
# parser.add_argument("--batch_size", type=int, default=16, help="Size of each training batch")
# parser.add_argument("--sequence_length", type=int, default=40, help="Number of frames in each sequence")
# parser.add_argument("--img_dim", type=int, default=224, help="Height / width dimension")
# parser.add_argument("--channels", type=int, default=3, help="Number of image channels")
# parser.add_argument("--latent_dim", type=int, default=512, help="Dimensionality of the latent representation")
# parser.add_argument("--checkpoint_model", type=str, default="", help="Optional path to checkpoint model")
# parser.add_argument(
#     "--checkpoint_interval", type=int, default=5, help="Interval between saving model checkpoints"
# )
# opt = parser.parse_args()
# print(opt)



if __name__ == '__main__':
    torch.manual_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    
    params={}
    batch_size = 128
    learn_rate = 0.4
    num_of_epochs = 100
    image_size = 64
    site = 1302
    #betas =
    #device = TBD
    
    ### Load dataset 
    years = range(2010,2021)
    matches_pm_crops_files=[]
    for year in years:
        matches_pm_crops_file = '/home/adiraz/adiraz/output/crops/crops_and_pm_values_{}.json'.format(year)
        matches_pm_crops_files.append(matches_pm_crops_file)
        
    ds = PM_Images_Dataset(matches_pm_crops_files,image_size = image_size)
    split_lengths = [int(len(ds) * 0.9),len(ds) -int(len(ds) * 0.9)]
    ds_train, ds_test = random_split(ds, split_lengths)
    dl_train = DataLoader(ds_train, batch_size, shuffle=True,num_workers = 8)
    dl_test = DataLoader(ds_test, batch_size, shuffle=True, num_workers= 8)
    
    ### Initialize Model    
    model = PM_Predictor(params).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learn_rate)#, betas=betas)
    loss_func = MSELoss()
    model.train()
    loss_per_epoch = []

    for epoch_idx, epoch in enumerate(range(num_of_epochs)):
        epoch_loss = 0
        with tqdm.tqdm(total=len(dl_train.batch_sampler), file=sys.stdout) as pbar:
          #  t = time.time()
            for batch_idx, (images, labels) in enumerate(dl_train):
           #     elapsed = time.time() - t
                images = images.to(device)
                labels = labels.to(device).view((len(labels),1))
                optimizer.zero_grad()
                predicted_pm = model(images)
                #labels = labels.unsqueeze(0)
                loss = loss_func(predicted_pm,labels)
                loss.backward()
                optimizer.step()
                epoch_loss+=loss
                pbar.update()
            #    t=time.time()

            loss_per_epoch=epoch_loss/batch_size
        print("Epoch loss: ", loss_per_epoch)

        if epoch_idx%10 == 0:
            total_loss = 0
            with torch.no_grad():
                for batch_idx, (images, labels) in enumerate(dl_test):
                    images = images.to(device)
                    labels = labels.to(device).view((len(labels),1))
                    optimizer.zero_grad()
                    predicted_pm = model(images)
                    loss = loss_func(predicted_pm,labels)
                    print(loss)
    #train()



