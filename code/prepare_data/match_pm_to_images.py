import json
import numpy as np
import xarray as xr
import rioxarray as rxr
from misr_data import MISR_Data
import os

class PM_Data:
    def __init__(self, file):
        self.pm_file = file

    def load(self):
        with open(self.pm_file) as f:
            pm_data =json.load(f)['Data']
            return pm_data



def check_if_pm_station_is_in_misr_image(pm_geo_location_lat,pm_geo_location_lon, misr_geo_location):
    if pm_geo_location_lat > misr_geo_location['min_lat'] and pm_geo_location_lat < misr_geo_location['max_lat'] and \
            pm_geo_location_lon > misr_geo_location['min_lon'] and pm_geo_location_lon < misr_geo_location['max_lon']:
        return True
    else:
        return False


def find_matches_between_pm_to_misr_data(pm_data_file,misr_dir):
    matches_misr_pm_data = []

    pd = PM_Data(pm_data_file)
    pm_data = pd.load()
    misr_subset_dir = misr_dir
    misr_files = [os.path.join(misr_subset_dir,f) for f in os.listdir(misr_subset_dir) if f.endswith('hdf')]
    misr_files_per_date = {}
    for file in misr_files:
        print('reading file ', file)
        misr = MISR_Data(file)
        misr_date = misr.get_date()
        if misr_date not in misr_files_per_date.keys():
            misr_files_per_date[misr_date]  = []
        misr_files_per_date[misr_date].append({'file_name':  file , 'blocks_geo_locations' : misr.get_max_min_lon_lat_per_block()})

    pm_data_per_date = {}
    for pm_measure in pm_data:
        pm_date = pm_measure['date_gmt']
        if pm_date not in pm_data_per_date:
            pm_data_per_date[pm_date] =[]
        pm_data_per_date[pm_date].append(pm_measure)

    #check date convention
    for date in pm_data_per_date.keys():
        for pm_station_data in pm_data_per_date[date]:
            pm_geo_location_lat = pm_station_data['latitude']
            pm_geo_location_lon = pm_station_data['longitude']
            if date in misr_files_per_date.keys():
                misr_data_from_this_date = misr_files_per_date[date]
                for misr_file in misr_data_from_this_date:
                    misr_blocks_geo_location = misr_file['blocks_geo_locations']
                    for bidx, misr_geo_location in enumerate(misr_blocks_geo_location):
                        if check_if_pm_station_is_in_misr_image(pm_geo_location_lat,pm_geo_location_lon,misr_geo_location):
                            matches_misr_pm_data.append({'pm_data': pm_station_data, 'image_data' : {'file' : misr_file , 'block' : bidx}})
                        print('Found match!')

    return matches_misr_pm_data

pm_data_file = '/Users/adirazgoldfarb/Yoav Shechner/images_to_pm/pm_data/la_pm_2021.json'
misr_dir = '/Users/adirazgoldfarb/Yoav Shechner/data_subset'
matches_misr_pm_data = find_matches_between_pm_to_misr_data(pm_data_file,misr_dir)
matches_file = '/Users/adirazgoldfarb/Yoav Shechner/images_to_pm/matches_pm_misr.json'
with open(matches_file,'w') as f:
    json.dump(matches_misr_pm_data,f)