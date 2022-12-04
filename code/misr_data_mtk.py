import MisrToolkit as mtk
import numpy as np
import cv2
GRID_LIST = ['BlueBand',
 'GreenBand',
 'RedBand',
 'NIRBand']

FIELDS_LIST = ['Blue Radiance/RDQI','Green Radiance/RDQI','Red Radiance/RDQI', 'NIR Radiance/RDQI']

class MISR_Data:
    def __init__(self, file):
        self.misr_file = mtk.MtkFile(file)
        self.work_resolution = [128,512]
        
    def get_block(self, block):
        channels = []
        for grid,field in zip(GRID_LIST, FIELDS_LIST):
            g = self.misr_file.grid(grid)
            scale_factor = g.attr_get('Scale factor')
            f = g.field(field)
            c = f.read(block,block)
            datas = np.right_shift(c[0],2)
            fva = f.fill_value
            _FillValue = fva
            dataf = datas.astype(np.double)
            dataf[datas == _FillValue] = np.nan
            dataf[ datas > 16376] = np.nan
            if dataf.shape[0] > self.work_resolution[0]:
                image_scale = 0.25
                dataf = cv2.resize(dataf,(0,0),fx = image_scale,fy=image_scale, interpolation = cv2.INTER_CUBIC)
            datam = np.ma.masked_array(dataf,mask= np.isnan(dataf))
            datam = scale_factor * datam
            channels.append(datam)
        block_image = np.ma.stack(channels,axis = 0)
        return block_image