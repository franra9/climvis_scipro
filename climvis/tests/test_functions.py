"""Test file for all the functions in functions.py"""

from climvis.functions import process_date, era5_pos, variables_to_download, \
    clim, yearly_evol, path
import xarray as xr
import numpy as np
import pytest
import os

# Path to data folder
file_dir = path()


def test_era5_pos():
    # Author: Marie Schroeder
    # check for a positive given longitude
    lon, lat = era5_pos(136.34, 23.78)

    assert lon == 316.25
    assert lat == 23.75

    # check for a negative given longitude
    lon, lat = era5_pos(-33.96, 23.1)

    assert lon == 146
    assert lat == 23

    # check for 0 longitude
    lon, lat = era5_pos(0, 0)

    assert lon == 180
    assert lat == 0

    # check that an error is issued when abs(lat)>90 or abs(lon)>180
    with pytest.raises(ValueError):
        era5_pos(190, 40)
    with pytest.raises(ValueError):
        era5_pos(150, 100)
    with pytest.raises(ValueError):
        era5_pos(190, 100)

def test_process_date():
    # Author: Marie Schroeder
    # check if 2 years give the range of years and all 12 months
    start_year = "1985"
    end_year = "1988"
    start_month = "1"
    end_month = "2"

    year_range, month_range = process_date(start_year, start_month,
                                           end_year, end_month)
    assert ["1985", "1986", "1987", "1988"] == year_range
    assert ["01", "02", "03", "04", "05", "06", "07", "08", "09",
            "10", "11", "12"] == month_range

    # check if the same year only gives one string in year_range and correct
    # range of months
    start_year = "1985"
    end_year = "1985"
    start_month = "1"
    end_month = "9"

    year_range, month_range = process_date(start_year, start_month, end_year,
                                           end_month)
    assert ["1985"] == year_range
    assert ["01", "02", "03", "04", "05", "06", "07", "08",
            "09"] == month_range

    # check if month list gets sorted right if not all 12 months are used
    start_year = "1985"
    end_year = "1986"
    start_month = "10"
    end_month = "3"

    year_range, month_range = process_date(start_year, start_month, end_year,
                                           end_month)
    assert ["1985", "1986"] == year_range
    assert ["01", "02", "03", "10", "11", "12"] == month_range


def test_variables_to_download():
    # Author: Gorosti Mancho
    # Checks if for two given variables of interest the proper variables
    # that need to be downloaded are obtained

    # Check for variables that require more than one variable to be downloaded

    variables = ['Snow Depth', 'Energy Budget']
    chosen_variables, regions = variables_to_download(variables)

    reference_solution = ['snow_depth', 'snow_density',
                          'surface_latent_heat_flux',
                          'surface_net_solar_radiation',
                          'surface_net_thermal_radiation',
                          'surface_sensible_heat_flux']
    reference_solution_enso = []

    assert reference_solution == chosen_variables
    assert reference_solution_enso == regions

    # Check for variables that only require one variable to be downloaded

    variables = ['Temperature at 2m', 'Friction Velocity']
    chosen_variables, regions = variables_to_download(variables)

    reference_solution = ['2m_temperature', 'friction_velocity']
    reference_solution_enso = []

    assert reference_solution == chosen_variables
    assert reference_solution_enso == regions

    # Check for ENSO variables

    variables = ['ENSO en12', 'ENSO en3']
    chosen_variables, regions = variables_to_download(variables)

    reference_solution = []
    reference_solution_enso = ['en12', 'en3']

    assert reference_solution == chosen_variables
    assert reference_solution_enso == regions


# Test clim output
def test_clim():
    # Author: Francesc Roura Adserias
    # Check that the output given a test netCDF is a xr.Dataset of length 12
    climate = clim(os.path.join(file_dir, "testfile.nc"))
    assert type(climate) == xr.Dataset
    assert len(np.array(climate.sst)) == 12


# Test yearly_evol for different known prebuilt cases
def test_evol():
    # Author: Francesc Roura Adserias
    climate = clim(os.path.join(file_dir, "testfile.nc"))

    # check that output length is consistent
    ano1 = yearly_evol(climate, os.path.join(file_dir, "testfile.nc"), 1998, 2000, 12, 2)
    ano2 = yearly_evol(climate, os.path.join(file_dir, "testfile.nc"), 1999, 2000, 2, 12)
    ano3 = yearly_evol(climate, os.path.join(file_dir, "testfile.nc"), 2000, 2000, 1, 2)
    assert len(np.array(ano1)) == 15  # ((2000 - 1998 - 1) * 12 + 3)
    assert len(np.array(ano2)) == 23
    assert len(np.array(ano3)) == 2

    # check that an error is issued when wrong period is entered
    with pytest.raises(ValueError):
        yearly_evol(climate, os.path.join(file_dir, "testfile.nc"), 2000, 1999, 2, 1)
