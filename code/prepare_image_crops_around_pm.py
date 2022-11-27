import os
from PIL import Image
import cv2
import json
from misr_data import MISR_Data
import numpy as np



def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    idxs = np.unravel_index(idx, array.shape)
    return idxs


def get_image_around_pm_measurement(pm_loc, image_data):
    image_file = image_data['file']['file_name']
    block_id = image_data['block']
    misr = MISR_Data(image_file)
    images, latitude, longitude = misr.load_block(block_id)
    # latitude and lingtidue are provided in full resolution
    # ( like red channel, check interpolation type!! )
    latitude = cv2.resize(latitude, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
    longitude = cv2.resize(longitude, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
    idxs = find_nearest(latitude,pm_loc['latitude'])
    box_size= 16
    box_half_size = box_size//2
    if idxs[0] < box_half_size or idxs[0]  < box_half_size:
        return []
    left, upper, right, lower = idxs[1] - box_half_size, idxs[0]-box_half_size, idxs[1] + box_half_size,idxs[0]+box_half_size
    box = [left,upper,right,lower]
    all_channels_images = []
    for image in images:
        pil_image = Image.fromarray(image)
        cropped = pil_image.crop(box)
        all_channels_images.append(cropped)
        #all_channels_np_array = np.stack(all_channels_images,axis=0)
    #return all_channels_np_array
    return all_channels_images



matches_pm_images_file = '/Users/adirazgoldfarb/Yoav Shechner/images_to_pm/matches_pm_misr.json'
crops_output_foler = '/Users/adirazgoldfarb/Yoav Shechner/images_to_pm/crops'
matches_pm_crops_file = '/Users/adirazgoldfarb/Yoav Shechner/images_to_pm/matches_pm_misr_crops.json'

os.makedirs(crops_output_foler,exist_ok=True)
with open(matches_pm_images_file) as f:
    pm_images_matches = json.load(f)

pm_crops_matches = []
for match_idx , pm_image_match in enumerate(pm_images_matches):
    pm_data = pm_image_match['pm_data']
    pm_label = pm_data['sample_measurement']
    if pm_label is None:
        continue
    pm_loc = {'latitude' : pm_data['latitude'], 'longitude': pm_data['longitude']}
    image_data = pm_image_match['image_data']
    image_file_name = os.path.basename(image_data['file']['file_name']).split('.')[0]

    image = get_image_around_pm_measurement(pm_loc,image_data)
    if len(image) > 0 :
        crop_file_name = os.path.join(crops_output_foler,"{:06}".format(match_idx) + '_' + image_file_name  +'.tiff')
        image[0].save(crop_file_name, format="tiff", append_images=[image[1],image[2],image[3]], save_all=True, duration=500, loop=0)
        pm_crops_matches.append({'pm_label': pm_label, 'image_path' : crop_file_name})
    #pil_im = Image.fromarray(image)
    #pil_im.save(crop_file_name)

with open(matches_pm_crops_file,'w') as f:
    json.dump(pm_crops_matches,f)