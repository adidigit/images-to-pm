import torch

from torch.utils.data import Dataset
import os
import random
from PIL import Image
from torchvision.io import read_image
from PIL import Image
import cv2
import json
from misr_data import MISR_Data
import numpy as np
import torchvision.transforms as T


class PM_Images_Dataset(Dataset):
    def __init__(self, matches_pm_crops_file ,image_size = 32, transform=None):
        self.transform = transform
        self.image_size = image_size
        self.scale_transform = T.Resize((self.image_size, self.image_size))
        with open(matches_pm_crops_file) as f:
            self.pm_crops_matches = json.load(f)
        #random.shuffle(self.pm_crops_matches)

    def __len__(self):
        return len(self.pm_crops_matches)

    def __getitem__(self, idx):
        pm_image_match = self.pm_crops_matches[idx]
        label = pm_image_match['pm_label']
        image_4d = Image.open(pm_image_match['image_path'])
        images_array = np.zeros([4,self.image_size,self.image_size])
        if image_4d.n_frames != 4:
            return "Error in Tiff image, missing channel!"
        for i in range(image_4d.n_frames):
            #iterate over PIL images:
            image_4d.seek(i)
            if self.image_size != image_4d.size[0] :
                im = self.scale_transform(image_4d)
                #im  = self.transform(im)
                images_array[i,:,:] =  np.array(im)
        return torch.FloatTensor(images_array) , torch.tensor(label)

if __name__ == '__main__':
    matches_pm_crops_file = '/Users/adirazgoldfarb/Yoav Shechner/images_to_pm/matches_pm_misr_crops.json'
    ds = PM_Images_Dataset(matches_pm_crops_file)
    image , pm_label = ds[0]
    pass