from pm_data import PM_Data
from misr_tabular_data import MISR_tabular_data, get_misr_data_df
import pandas
import MisrToolkit as mtk
import numpy as np
import json

pm_data_file = '/home/adiraz/adiraz/misr_data/pm_la_2019.json'
misr_dir = '/home/adiraz/adiraz/misr_data'
output_file = '/home/adiraz/adiraz/misr_data/misr_pm_matches.json'
all_matches = [] # global

def get_relevant_images(p) :
    pm_val = p['arithmetic_mean']
    date = p['date_local'] 
    path_pixels = p['pm_pixels_location']
    for path in path_pixels.keys():
        all_relevant_images = misr_df.loc[(misr_df['date'] == date) & (misr_df['path'] == path),'file_name']
        if len(all_relevant_images)> 0 :
            all_matches.append({'pm_val' : pm_val, 'images' : list(all_relevant_images)})
    return all_relevant_images


pdaily = PM_Data(pm_data_file)
pm_data = pdaily.load()
misr_df = get_misr_data_df(misr_dir)
pm_data['pm_pixel_location'] = np.empty((len(pm_data), 0)).tolist()
all_sites = pm_data['site_number'].unique()
paths_per_site = {}
all_misr_available_paths = misr_df['path'].unique()
resolution = 1100
for site in all_sites:
    lat = pm_data[pm_data['site_number'] == site]['latitude'].head(1)
    lon = pm_data[pm_data['site_number'] == site]['longitude'].head(1)
    all_path_data = dict.fromkeys(all_misr_available_paths)
    for path in all_misr_available_paths:
        try:
            site_pixel_location = mtk.latlon_to_bls(path, resolution, float(lat),float(lon))
            all_path_data[path] = site_pixel_location
        except:
            continue
    arr = np.empty(len(pm_data.loc[pm_data['site_number'] == site]), dtype=object)
    arr[:] = [all_path_data for i in range(len(arr))]
    pm_data.loc[pm_data['site_number'] == site, 'pm_pixels_location'] = arr 

pm_data.apply(get_relevant_images,axis=1)
with open(output_file,'w') as f:
    json.dump(all_matches,f)