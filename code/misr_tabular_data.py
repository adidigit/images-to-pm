import os
import re
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import mpl_toolkits.basemap.pyproj as pyproj
import numpy as np
#from mpl_toolkits.basemap import Basemap
#from pyhdf.SD import *
#import xarray as xr
#import rioxarray as rxr
#import cv2
import pandas
import MisrToolkit as mtk

def get_misr_data_df(misr_dir):
    misr_files = [os.path.join(misr_dir,f) for f in os.listdir(misr_dir) if f.endswith('hdf')]
    all_data = []
    for i, file in enumerate(misr_files):
        misr = MISR_tabular_data(file)
        d = {'file_name': file ,
             'date' : misr.get_date() , 
             'orbit': misr.get_orbit(), 
             'path' : misr.get_path(), 
             'camera' : misr.get_camera() }
        all_data.append(d)

    df = pandas.DataFrame(all_data)
    return df

class MISR_tabular_data:
    def __init__(self,file):
        self.misr_file = mtk.MtkFile(file)
    
    def get_date(self):
        m =  self.misr_file # ,mask_and_scale=True)
        times = m.block_metadata_field_read('PerBlockMetadataTime','BlockCenterTime')
        a = [ t for t in times if t is not '' ]
        date = a[1]
        date = pandas.to_datetime(date).date()
        self.date = str(date)
        #m.core_metadata_get (EQUATORCROSSINGTIME)
        return str(date)
    
    def get_path(self):
        m =  self.misr_file 
        path = m.attr_get('Path_number')
        return path
    
    def get_orbit(self):
        m =  self.misr_file 
        orbit = m.core_metadata_get('ORBITNUMBER')
        return orbit
    
    def get_camera(self):
        m =  self.misr_file
        cam = m.attr_get('Camera')
        return cam
        