import os
from PIL import Image
import cv2
import json
#from misr_data import MISR_Data
from misr_data_mtk import MISR_Data
import numpy as np



def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    idxs = np.unravel_index(idx, array.shape)
    return idxs


def get_image_around_pm_measurement(pm_loc, image_file):
    block_id = image_file['block']
    misr = MISR_Data(image_file)
    images, latitude, longitude = misr.load_block(block_id)
    # latitude and lingtidue are provided in full resolution
    # ( like red channel, check interpolation type!! )
    latitude = cv2.resize(latitude, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
    longitude = cv2.resize(longitude, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
    idxs = find_nearest(latitude,pm_loc['latitude'])
    box_size= 16
    box_half_size = box_size//2
    if idxs[0] < box_half_size or idxs[1]  < box_half_size:
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

def get_images_around_pm_measurement(pm_loc, images_files,block,pixel_xy):
    
    multi_angle_images_list = []
    for image_file in images_files:
        misr = MISR_Data(image_file)
        multi_channnel_image = misr.get_block(block)
        multi_angle_images_list.append(multi_channnel_image)
    multi_angle_image = np.ma.concatenate(multi_angle_images_list,axis=0)
    box_size= 16
    box_half_size = box_size//2
    if pixel_xy[0] < box_half_size or pixel_xy[1]  < box_half_size:
        print('station is out of box', pixel_xy)
        return []
    left, upper, right, lower = pixel_xy[0] - box_half_size, pixel_xy[1]-box_half_size, pixel_xy[0] + box_half_size,pixel_xy[1]+box_half_size
    box = [left,upper,right,lower]
    multi_angle_crops = []
    for image in multi_angle_image:
        pil_image = Image.fromarray(image)
        cropped = pil_image.crop(box)
        multi_angle_crops.append(cropped)
    return multi_angle_crops

if __name__ == '__main__':
    pm_data_types_options = ['row', 'daily']
    pm_data_type = 'daily'
    
    for year in range(2010,2021):
        matches_pm_images_file = '/home/adiraz/adiraz/output/pm_misr_matches/pm_misr_matches_{0}.json'.format(year)
        crops_output_foler = '/home/adiraz/adiraz/output/crops/{0}'.format(year)
        matches_pm_crops_file = '/home/adiraz/adiraz/output/crops/crops_and_pm_values_{0}.json'.format(year)

        os.makedirs(crops_output_foler,exist_ok=True)
        with open(matches_pm_images_file) as f:
            pm_images_matches = json.load(f)

        pm_crops_matches = []
        for match_idx , pm_image_match in enumerate(pm_images_matches):
            #print(match_idx)
            pm_data = pm_image_match['pm_data']
            if pm_data_type == 'row':
                pm_label = pm_data['sample_measurement']
            if pm_data_type == 'daily':
                pm_label = pm_data['arithmetic_mean']
            if pm_label is None:
                continue
            pm_site = pm_data['site_number']
            pm_loc = {'latitude' : pm_data['latitude'], 'longitude': pm_data['longitude']}
            images = pm_image_match['images']
            date = pm_data['date_local']
            for path_num in images.keys():
                if pm_data['pm_pixels_location'][path_num] is not None:
                    block = pm_data['pm_pixels_location'][path_num][0]
                    line = pm_data['pm_pixels_location'][path_num][1]
                    sample =  pm_data['pm_pixels_location'][path_num][2]
                    pixel_xy = (sample,line)
                    images_crops = get_images_around_pm_measurement(pm_loc,images[path_num],block, pixel_xy)
                    if len(images_crops) > 0 :
                        image_name = images[path_num][0].split('/')[-1].split('.')[0]
                        crop_file_name = os.path.join(crops_output_foler,"{:06}".format(match_idx) + '_' + pm_site + '_' + path_num  + '_' + date + '.tiff')
                        images_crops[0].save(crop_file_name, format="tiff", append_images=images_crops[1:], save_all=True, duration=500, loop=0)
                        pm_crops_matches.append({'pm_label': pm_label, 'image_path' : crop_file_name})
                    else:
                        print('station {0} crop is out of bound'.format(pm_site))
            #pil_im = Image.fromarray(image)
            #pil_im.save(crop_file_name)

        with open(matches_pm_crops_file,'w') as f:
            json.dump(pm_crops_matches,f)