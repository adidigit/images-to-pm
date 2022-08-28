import json
import numpy as np
import xarray as xr
import rioxarray as rxr

class PM_Data:
    def __init__(self, file):
        self.pm_file = file

    def load(self):
        with open(self.pm_file) as f:
            pm_data =json.load(f)['Data']
            return pm_data

import os
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
#import mpl_toolkits.basemap.pyproj as pyproj
import numpy as np
#from mpl_toolkits.basemap import Basemap
from pyhdf.SD import *
import xarray as xr
import rioxarray as rxr

class MISR_Data:
    def __init__(self,misr_file,prefix = 'MISR_AM1_GRP_ELLIPSOID_GM_'):
        self.misr_file = misr_file
        self.prefix = prefix

    def get_date(self):
        misr = rxr.open_rasterio(self.misr_file)  # ,mask_and_scale=True)
        try:
            attrs = misr[0].attrs
            date = attrs['EQUATORCROSSINGDATE.1']
        except:
            attrs = misr.attrs
            date = attrs['EQUATORCROSSINGDATE.1']
        return date


    def load(self):
        misr = rxr.open_rasterio(self.misr_file)  # ,mask_and_scale=True)
        try:
            attrs = misr[0].attrs
        except:
            attrs = misr.attrs
        self.date = attrs['EQUATORCROSSINGDATE.1']
        self.start_block = int(attrs['Start_block' ])
        self.end_block = int(attrs['End block'])
        self.blocks = np.arange(self.start_block,self.end_block,dtype='int')
        self.scale_factor = 1
        self.hdf = SD(self.misr_file, SDC.READ)
        images = self.get_blocks_images()
        latitude, longitude = self.get_latitude_longitude()
        return images, latitude, longitude
    #("BlueBand|Blue Radiance/RDQI", "GreenBand|Green Radiance/RDQI",
    # "NIRBand|NIR Radiance/RDQI", "RedBand|Latitude", "RedBand|Longitude", "RedBand|Red Radiance/RDQI")
    def get_channel(self,channel_name,block_num):
        print('Reading channel ', channel_name)
        data3D = self.hdf.select(channel_name)
        block_num = int(block_num)
        data = data3D[block_num, :, :]
        attrs = data3D.attributes(full=1)
        fva = attrs["_FillValue"]
        _FillValue = fva[0]
        datas = np.right_shift(data, 2);
        dataf = datas.astype(np.double)
        dataf[data == _FillValue] = np.nan
        dataf[datas > 16376] = np.nan
        datam = np.ma.masked_array(dataf, mask=np.isnan(dataf))
        datam = self.scale_factor * datam;
        return datam

    def get_image(self,block_num):
        channels = [ 'Red Radiance/RDQI', 'Green Radiance/RDQI','Blue Radiance/RDQI', 'NIR Radiance/RDQI']
        scale_factor = 1
        channels_list = []
        for channel_name in channels:
            ch = self.get_channel(channel_name,block_num)
            channels_list.append(ch)
        channels_im = np.array(channels_list)
        return channels_im

    def get_blocks_images(self):
        blocks_images = []
        for block_num in self.blocks:
            block_im = self.get_image(block_num)
            blocks_images.append(block_im)
        return blocks_images

    def parse_file_name(self):
        file_name_start = self.misr_file.find(self.prefix)
        data_to_parse = self.misr_file[file_name_start:]
        path_number = data_to_parse[1:4]
        orbit_number = data_to_parse[6:12]
        camera = data_to_parse[13:15]
        start_block_data = data_to_parse.find('.')
        block_data_to_parse = data_to_parse[start_block_data:]
        self.start_block = block_data_to_parse[1:4]
        self.end_block = block_data_to_parse[5:8]

    def get_latitude_longitude(self):
        blocks_latitude = []
        blocks_longitude = []
        lat = self.hdf.select('Latitude')
        lon = self.hdf.select('Longitude')
        for block_num in self.blocks:
            block_num = int(block_num)
            block_lat = lat[block_num,:,:]
            block_lon = lon[block_num,:,:]
            blocks_latitude.append(block_lat)
            blocks_longitude.append(block_lon)
        return blocks_latitude,blocks_longitude

    def get_max_min_lon_lat(self):
        #change this after understaning how to read it crrectly
        #misr = rxr.open_rasterio(self.misr_file)  # ,mask_and_scale=True)

        images , latitude, longitude = self.load()
        lat_lon_ranges = {}
        lat_lon_ranges['min_lat'] = np.min(latitude)
        lat_lon_ranges['max_lat'] = np.max(latitude)
        lat_lon_ranges['min_lon'] = np.min(longitude)
        lat_lon_ranges['max_lon'] = np.max(longitude)

        return lat_lon_ranges


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
        misr_files_per_date[misr_date].append({'file_name':  file , 'geo_location' : misr.get_max_min_lon_lat()})

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
                    misr_geo_location = misr_file['geo_location']
                    if check_if_pm_station_is_in_misr_image(pm_geo_location_lat,pm_geo_location_lon,misr_geo_location):
                        matches_misr_pm_data.append({'pm_data': pm_station_data, 'misr_data' : misr_file})
                        print('Found match!')

    return matches_misr_pm_data

pm_data_file = '/Users/adirazgoldfarb/Yoav Shechner/images_to_pm/pm_data/la_pm_2021.json'
misr_dir = '/Users/adirazgoldfarb/Yoav Shechner/data_subset'
matches_misr_pm_data = find_matches_between_pm_to_misr_data(pm_data_file,misr_dir)

