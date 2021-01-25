"""This configuration module is a container for parameters and constants."""
import os
import sys

#cru_dir = r'C:\Users\marie\Documents\UNI\Master\Semester_1\Programming\ClimVis\climvis-master\climvis\data'
#cru_tmp_file = cru_dir + '\cru_ts4.03.1901.2018.tmp.dat.nc'
#cru_pre_file = cru_dir + '\cru_ts4.03.1901.2018.pre.dat.nc'
#cru_topo_file = cru_dir + '\cru_cl1_topography.nc'

# The program checks if you have the .climvis file with the path to the data and if not asks you the path to the data
# and creates the .climvis file
home = os.path.expanduser("~")
file_name = ".climvis"
file_path = os.path.join(home, file_name)

if not os.path.exists(file_path):
    cru_dir = input("Please enter the path to the folder with the CRU data:")
    cru_tmp_file = os.path.join(os.path.realpath(cru_dir), 'cru_ts4.03.1901.2018.tmp.dat.nc')
    cru_pre_file = os.path.join(os.path.realpath(cru_dir), 'cru_ts4.03.1901.2018.pre.dat.nc')
    cru_topo_file = os.path.join(os.path.realpath(cru_dir), 'cru_cl1_topography.nc')

    if os.path.exists(cru_tmp_file) or os.path.exists(cru_pre_file) or os.path.exists(cru_topo_file):
        file = open(file_path, "w")
        file.write(os.path.realpath(cru_dir))
        file.close()
    else:
        print("The path to the CRU data you entered is not working. Please enter a valid path.")

else:
    path = open(file_path)
    cru_dir = path.read()
    cru_tmp_file = os.path.join(os.path.realpath(cru_dir), 'cru_ts4.03.1901.2018.tmp.dat.nc')
    cru_pre_file = os.path.join(os.path.realpath(cru_dir), 'cru_ts4.03.1901.2018.pre.dat.nc')
    cru_topo_file = os.path.join(os.path.realpath(cru_dir), 'cru_cl1_topography.nc')

bdir = os.path.dirname(__file__)
html_tpl = os.path.join(bdir, 'data', 'template.html')
world_cities = os.path.join(bdir, 'data', 'world_cities.csv')

default_zoom = 8
