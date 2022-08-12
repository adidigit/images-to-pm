
# download MISR data
#https://forum.earthdata.nasa.gov/viewtopic.php?t=2330&sid=44719a1b0b5c9e1703e0154a594cbcdc
#https://asdc.larc.nasa.gov/data/MISR/

import requests
from pathlib import Path

url=<the URL of the file you want to download>
token=<your token>
header={"Authorization": f"Bearer {token}"}

response = requests.get(url, headers=header)
content = response.content
file_name = url.split('/')[-1]
data_path = Path(file_name)
data_path.write_bytes(content)


import xarray as xr
import rioxarray as rxr

def extract_misr_image(misr_hdf_file):
    misrcvo = rxr.open_rasterio(misr_hdf_file)  # ,masked=True)

