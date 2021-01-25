"""Tests if all the functions work correctly together"""

import matplotlib.pyplot as plt
from climvis.functions import process_date, era5_pos, variables_to_download
from climvis.functions import clim, yearly_evol, path
from climvis.download import download_era5, dwl_era5_enso
from climvis.plots import final_plot
import os
import numpy as np

start_year = "2017"
start_month = "01"
end_year = "2018"
end_month = "03"
date = [start_year, end_year, start_month, end_month]

lon = 11.0
lat = 45.0

variables = ["Energy Budget", "Temperature at 2m"]

fig, ax = plt.subplots()

# path to data folder
file_dir = path()

file = os.path.join(file_dir, "integral_test.nc")


def test_integral():
    # Author: Marie Schroeder
    longitude, latitude = era5_pos(lon, lat)
    # check that longitude and latitude are right
    assert latitude == lat
    assert longitude == lon + 180

    year_range, month_range = process_date(start_year, start_month,
                                           end_year, end_month)
    # check if right year and month range are created
    month_range_test = list(range(1, 13))
    month_range_test = ["{0:0=2d}".format(i) for i in month_range_test]
    assert year_range == ["2017", "2018"]
    assert month_range == month_range_test

    chosen_variables, regions = variables_to_download(variables)
    # check if right variables got chosen
    assert chosen_variables == ['surface_latent_heat_flux',
                                'surface_net_solar_radiation',
                                'surface_net_thermal_radiation',
                                'surface_sensible_heat_flux',
                                '2m_temperature']
    assert regions == []  # because no enso is chosen

    download_era5(chosen_variables, year_range, month_range, file)
    # check if file gets downloaded
    assert os.path.exists(file_dir + "/integral_test.nc")

    not_important, ax_test = final_plot(date, variables, fig, longitude,
                                        latitude, file)
    # check if something is plotted
    assert ax_test.lines != []
    # check if title is right
    assert ax_test.get_title() == "Energy Budget vs Temperature at 2m at " \
                                  "Longitude = 11.0º and Latitude = 45.0º"


# enso integral test
smonth = 2
fmonth = 5
syear = 1981
fyear = 1981
region = "en12"
filein = os.path.join(file_dir, 'ERA5_Monthly_sst_' + str(fyear) + '_' + region + '.nc')


def test_integral_enso():
    # Author: Francesc Roura Adserias
    dwl_era5_enso(fyear, region, filein)
    cli = clim(filein)
    ano1 = yearly_evol(cli, filein, syear, fyear, smonth, fmonth)
    # Check known result
    a = (np.array(ano1) == np.float32([-1.4777832, -0.6584778, -0.4020691,
                                         -0.06237793]))
    assert a.all()
