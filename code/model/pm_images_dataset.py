import torch

from torch.utils.data import Dataset
import os
import random
from PIL import Image
from torchvision.io import read_image
from PIL import Image
import cv2
import json
import numpy as np
import torchvision.transforms as T


class PM_Images_Dataset(Dataset):
    def __init__(self, matches_pm_crops_files ,image_size = 32,num_of_channels = 4, num_of_angles = 9, site = None , transform=None):
        self.transform = transform
        self.image_size = image_size
        self.scale_transform = T.Resize((self.image_size, self.image_size))
        self.pm_crops_matches = []
        self.num_of_angles = num_of_angles
        self.num_of_channels = num_of_channels
        for matches_pm_crops_file in matches_pm_crops_files:
            with open(matches_pm_crops_file) as f:
                 data = json.load(f)
            self.pm_crops_matches.extend(data)
        if site is not None:
            filtered_matches = [i for i in self.pm_crops_matches if i['image_path'].split('/')[-1][7:11] == str(site)]
            print(" taking only data from site " , site)
            self.pm_crops_matches = filtered_matches
            print("Num of samples: ", len(self.pm_crops_matches))
        random.shuffle(self.pm_crops_matches)

    def __len__(self):
        return len(self.pm_crops_matches)

    def __getitem__(self, idx):
        pm_image_match = self.pm_crops_matches[idx]
        label = pm_image_match['pm_label']
        image_4d = Image.open(pm_image_match['image_path'])
        images_array = np.zeros([self.num_of_angles*self.num_of_channels,self.image_size,self.image_size])
        if image_4d.n_frames !=self.num_of_angles*self.num_of_channels:
            return "Error in Tiff image, missing channel!"
        for i in range(image_4d.n_frames):
            #iterate over PIL images:
            image_4d.seek(i)
            if self.image_size != image_4d.size[0] :
                im = self.scale_transform(image_4d)
                #im  = self.transform(im)
            # add else condition
            #else:
            #    im =
                images_array[i,:,:] =  np.array(im)
        return torch.FloatTensor(images_array) , torch.tensor(label)

if __name__ == '__main__':
    
    #crops_dir = '/home/adiraz/adiraz/output/crops'
    #matches_pm_crops_files = [ i for i in os.listdir(crops_dir) if i.endwith('.json')]
    
    years = [2010] #range(2010,2021)
    matches_pm_crops_files =[]
    for year in years:
        matches_pm_crops_file = '/home/adiraz/adiraz/output/crops/crops_and_pm_values_{}.json'.format(year)
        matches_pm_crops_files.append(matches_pm_crops_file)
    
    ds = PM_Images_Dataset(matches_pm_crops_files)
    image , pm_label = ds[0]
    print(pm_label, image.shape)
    pass