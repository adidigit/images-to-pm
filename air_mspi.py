import h5py
import pandas
file_path = '/Users/adirazgoldfarb/Yoav Shechner/images_to_pm/AirMSPI_ER2_GRP_ELLIPSOID_20171023_184017Z_CA-Maricopa_SWPA_F01_V006.hdf'
f = h5py.File(file_path)

a = f['HDFEOS']

pandas.read_hdf(a)