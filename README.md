Pm data and misr data

1. pm data - daily pm data , in this file  
`file:///Users/adirazgoldfarb/Yoav%20Shechner/pm_data/la_pm_2021.json`  
taken from : https://aqs.epa.gov/data/api/sampleData/byCounty?email=test@aqs.api&key=test&param=88101&bdate=20210201&edate=20210501&state=06&county=037)  
See the parameters in the url that dictates the request.  
    each request is done up to one year, so we can ask for multiple times for different years, decided by states and counties
2. MIsr data - level 1b2 , data taken from here `https://asdc.larc.nasa.gov/data/MISR/MI1B2E.003/2021.02.03`
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

1. match_pm_to_images
2. prepare_image_crops_around_pm
3. use torch dataset in your training process.