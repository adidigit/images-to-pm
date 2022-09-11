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
import cv2
class MISR_Data:
    def __init__(self,misr_file,prefix = 'MISR_AM1_GRP_ELLIPSOID_GM_'):
        self.misr_file = misr_file
        self.prefix = prefix
        self.resolution = [128,512]

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

    def load_block(self,block_id):
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
        blocks_images_list = self.get_blocks_images()
        latitude, longitude = self.get_latitude_longitude()
        return blocks_images_list[block_id], latitude[block_id],longitude[block_id]

    def get_channel(self,channel_name,block_num,image_scale=1.):
        #print('Reading channel ', channel_name)
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
        if dataf.shape[0] > self.resolution[0] :
            image_scale = 0.25
            dataf = cv2.resize(dataf,(0,0),fx = image_scale,fy= image_scale, interpolation=cv2.INTER_CUBIC)
        datam = np.ma.masked_array(dataf, mask=np.isnan(dataf))
        datam = self.scale_factor * datam;
        return datam

    def get_4d_image(self, block_num):
        channels = [ 'Red Radiance/RDQI', 'Green Radiance/RDQI','Blue Radiance/RDQI', 'NIR Radiance/RDQI']
        scale_factor = 1
        channels_list = []
        for channel_name in channels:
            ch = self.get_channel(channel_name,block_num)
            channels_list.append(ch)
        channels_im = np.stack(channels_list,axis=0)
        return channels_im

    def get_blocks_images(self):
        blocks_images = []
        for block_num in self.blocks:
            block_im = self.get_4d_image(block_num)
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

    def get_max_min_lon_lat_per_block(self):
        #change this after understaning how to read it crrectly
        #misr = rxr.open_rasterio(self.misr_file)  # ,mask_and_scale=True)

        images , latitude, longitude = self.load()
        lat_lon_ranges_all_blocks = []
        for block_lat,block_lon in zip(latitude,longitude):
            lat_lon_ranges = {}
            lat_lon_ranges['min_lat'] = float(np.min(block_lat))
            lat_lon_ranges['max_lat'] = float(np.max(block_lat))
            lat_lon_ranges['min_lon'] = float(np.min(block_lon))
            lat_lon_ranges['max_lon'] = float(np.max(block_lon))
            lat_lon_ranges_all_blocks.append(lat_lon_ranges)
        return lat_lon_ranges_all_blocks
