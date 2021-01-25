"""Test file for all the functions in download.py"""

from climvis.download import download_era5, dwl_era5_enso
from climvis.functions import path
import os
import xarray as xr
import numpy as np
import pytest

# path to data folder
file_dir = path()


def test_download_era5():
    # Author: Marie Schroeder
    # test for 2 variables if file is downloaded and the right variables
    # are inside
    download_era5(["2m_temperature", "high_cloud_cover"], ["2019"],
                  ["01", "02"], os.path.join(file_dir, "test_download.nc"))
    data = xr.open_dataset(os.path.join(file_dir, "test_download.nc"))
    assert os.path.exists(os.path.join(file_dir, "test_download.nc"))
    assert np.any(data.t2m)


# dummy download
region = ["en12", "en3", "en34", "en4"]


def test_enso_dwl():
    # Author: Francesc Roura Adserias
    # Check that download works for every enso region:
    for re in region:
        dwl_era5_enso(2000, re, os.path.join(file_dir, 'ERA5_Monthly_sst_2000_' + re + '.nc'))
        print(re)
        filein = os.path.join(file_dir, 'ERA5_Monthly_sst_2000_' + re + '.nc')
        assert os.path.exists(filein)

        # Check ValueErrors rise correctly
    with pytest.raises(ValueError,
                       match='Arg "region" must be: "en12","en3","en34" or "en4".'):
        dwl_era5_enso(2000, "nao", os.path.join(file_dir, 'ERA5_Monthly_sst_2000_' + re + '.nc'))
    with pytest.raises(ValueError,
                       match='Final year must be in the 1979-2019 period.'):
        dwl_era5_enso(1714, "en12", os.path.join(file_dir, 'ERA5_Monthly_sst_2000_' + re + '.nc'))
