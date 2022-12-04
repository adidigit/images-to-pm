import sys

sys.path.append('../code')
from misr_data_mtk import MISR_Data
import json
from PIL import Image
import numpy as np
import cv2
#from pm_images_dataset import get_image_around_pm_measurement
from prepare_image_crops_around_pm import get_images_around_pm_measurement


    #lat_range = [pm_loc['latitude'] - 0.5 , pm_loc['latitude']+ 0.5]
    #lon_range = [pm_loc['longitude'] - 0.5 , pm_loc['longitude']+ 0.5]
    #lat_in_range = np.logical_and(latitude > lat_range[0] , latitude < lat_range[1])
    #lon_in_range = np.logical_and(longitude > lon_range[0] , longitude < lon_range[1])
    #idxs = np.where(np.logical_and(lat_in_range,lon_in_range))
    #left, upper, right, lower = np.min(idxs[1]), np.min(idxs[0]),np.max(idxs[1]),np.max(idxs[0])
    #np.where(latitude > pm_loc['latitude'] and)

def test_get_image_around_pm():
    matches_pm_images_file = '/home/adiraz/adiraz/output/pm_misr_matches/pm_misr_matches_2010.json'
    with open(matches_pm_images_file) as f:
        pm_images_matches = json.load(f)

    pm_image_match = pm_images_matches[3]
    pm_data = pm_image_match['pm_data']
    pm_label = pm_data['arithmetic_mean']
    pm_loc = {'latitude': pm_data['latitude'], 'longitude': pm_data['longitude']}
    path_num= list(pm_image_match['images'].keys())[0]
    image_data = pm_image_match['images'][path_num]
    block = pm_data['pm_pixels_location'][path_num][0]
    line = pm_data['pm_pixels_location'][path_num][1]
    sample =  pm_data['pm_pixels_location'][path_num][2]
    pixel_xy = (sample,line)
    image = get_images_around_pm_measurement(pm_loc, image_data,block,pixel_xy)
    return image

def check_multi_angle_image():
    tiff_file = '/Users/adirazgoldfarb/Yoav Shechner/images_to_pm/crops_v2_multiangle_9_only/000001_MISR_AM1_GRP_ELLIPSOID_GM_P039_O112443_AA_F03_0024.tiff'
    multi_angle_4d_images = Image.open(tiff_file)
    images_array = np.zeros([4*9, 16, 16])
    if multi_angle_4d_images.n_frames != 4*9:
        return "Error in Tiff image, missing channel!"
    for i in range(multi_angle_4d_images.n_frames):
        # iterate over PIL images:
        multi_angle_4d_images.seek(i)
        im = multi_angle_4d_images
        # im  = self.transform(im)
        images_array[i, :, :] = np.array(im)
    pass


#check_multi_angle_image()