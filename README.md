Pm data and misr data

1. pm data - raw pm data , in this file  
`file:///Users/adirazgoldfarb/Yoav%20Shechner/pm_data/la_pm_2021.json`  
taken from : 
https://aqs.epa.gov/data/api/sampleData/byCounty?email=test@aqs.api&key=test&param=88101&bdate=20210201&edate=20210501&state=06&county=037  
See the parameters in the url that dictates the request.  
    each request is done up to one year, so we can ask for multiple times for different years, decided by states and counties

daily avarage data
https://aqs.epa.gov/aqsweb/airdata/FileFormats.html ("Daily Summary Files")

4. MIsr data - level 1b2 , data taken from here `https://asdc.larc.nasa.gov/data/MISR/MI1B2E.003/2021.02.03`
local file is: `/Users/adirazgoldfarb/Yoav Shechner/misr_data/levelb2/MISR_AM1_GRP_ELLIPSOID_GM_P002_O112397_AA_F03_0024.hdf` ,   
There is a script for downloading data
3. Misr image data can be loaded by the relevant part in the jupyter notebook or by `extract_misr_images.py` , 
this is done for 1 file for 1 channel, need to be done for all angles and all channels.
4. Geo data - use the script [eos2dump](https://hdfeos.org/software/eosdump.php) to extract the laitutude and longtitude from hdd file by   
``` ./eos2dump -vcm2 ./levelb2/MISR_AM1_GRP_ELLIPSOID_GM_P002_O112397_AA_F03_0024.hdf BlueBand all > lon.txt```  
```./eos2dump -vcm1 ./levelb2/MISR_AM1_GRP_ELLIPSOID_GM_P002_O112397_AA_F03_0024.hdf BlueBand all > lat.txt```
.....https://hdfeos.org/zoo/NSIDC/AMSR_E_L3_DailyLand_V06_20050118.hdf.py...

misr downlad data interafces:

1.https://l0dup05.larc.nasa.gov/cgi-bin/MISR/main.cgi

https://search.earthdata.nasa.gov/search


## Data preperation
request blocks:
I took about 10 km from the farthest lat/lon of pm stations for each direction (0.1 degree) 
and checked the relevant blocks in misr block system:

39,63 39,64 40,63 40,64 41,63 41,64 42,63 43,62 43,63

https://search.earthdata.nasa.gov/search


1. match_pm_to_images
2. prepare_image_crops_around_pm
3. use torch dataset in your training process.

## versions:

v1 - couples of pm data and images that are cropped around
v2 - pm data is coupled with all images from orbit x ( 9 angles) that are matched to it.


## Open Issues:

1. terrain projection
2. find lat/lon in map - currently with KD TREE precision seems to be about 1 km - need to check if misr tool has someting better
3. latlon map resize - what is the best interpolation to use?


## server connection
IVANTI - vpn
****is_TOFFEE
ssh adiraz@132.68.58.178
GSHr*****90
cd adiraz


9.10.22
ORDER STATUS:
https://search.earthdata.nasa.gov/downloads/3702644641

18
problems with bashrc pythonpath, 
for using pip in conda use python -m pip...

cd adiraz
export PATH=~/home/adiraz/adiraz/miniconda3/bin:$PATH
conda activate pm36
jupyter lab --no-browser --port=8080

.. ( and then go to local computer and use SSH on the selected port)

ssh -L 8080:localhost:8080 adiraz@132.68.58.178

https://docs.anaconda.com/anaconda/user-guide/tasks/remote-jupyter-notebook/


https://search.earthdata.nasa.gov/downloads/4436620845 

  echo 'export PATH="/usr/local/opt/jpeg/bin:$PATH"' >> ~/.zshrc
era5
cams dust

dtm/ depth maps


dowmload all files from misr script:
copy all links to new file
wget --user user --password -i file.txt