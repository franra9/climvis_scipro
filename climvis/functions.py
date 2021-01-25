"""
A few important functions necessary for the end product are stored in this file.
"""

import xarray as xr
import numpy as np
import os
import datetime

plain_text_to_long = {
    "Temperature at 2m": "2m_temperature",
    "Lake Cover": "lake_cover",
    "Friction Velocity": "friction_velocity",
    "Cloud Base Height": "cloud_base_height",
    "Snow Albedo": "snow_albedo",
    "Sea Surface Temperature": "sea_surface_temperature",
    "Zonal Wind at 10 m": "10m_u_component_of_wind",
    "Meridional Wind at 10 m": "10m_v_component_of_wind",
    "Surface Pressure": "surface_pressure",
    "Soil Temperature": "soil_temperature_level_1",
    "Boundary Layer Height": "boundary_layer_height",
    "Low Cloud Cover": "low_cloud_cover",
    "Medium Cloud Cover": "medium_cloud_cover",
    "High Cloud Cover": "high_cloud_cover"
}


def path():
    """ Gives directory to the path of the data folder

    Returns
    -------
    file_dir : str
        Path to data folder

    """
    home = os.path.expanduser("~")
    file_name = ".era5vis"
    file_path = os.path.join(home, file_name)
    path = open(file_path)
    file_dir = path.read()
    return file_dir


def era5_pos(lon, lat):
    """ Returns nearest location available in the ERA5 dataset corresponding to
    the given location.

    Author: Marie Schroeder

    Parameters
    ----------
    lon : float
        The longitude
    lat : float
        The latitude

    Returns
    -------
    float
        Longitude and latitude available in ERA5

    Raises
    ------
    ValueError
        When longitude or latitude are out of range
    """

    # Check input
    if abs(lat) > 90 or abs(lon) > 180:
        raise ValueError('The given coordinates ({}, {}) '.format(lon, lat) +
                         'do not fit to the available data range.')

    # Compute
    dx = 180 + lon

    # Round to 0.25
    dx = float(round(dx * 4) / 4)
    lat = float(round(lat * 4) / 4)

    return dx, lat


def process_date(start_year, start_month, end_year, end_month):
    """ Gives back a range of years from the selected star year to end year and
    a range of months from the selected star month to end month.

    Author: Marie Schroeder

    Parameters
    ----------
    start_year: str
        The start year
    start_month: str
        The start month
    end_year: str
        The end year
    end_month: str
        The end month

    Returns
    --------
    year_range: list
        List of string with all the range of years
    month_range: list
        List of strings with all the range of months
    """

    if int(start_year) == int(end_year):
        year_range = [str(start_year)]
        month_range = list(range(int(start_month), int(end_month) + 1))
        month_range = ["{0:0=2d}".format(i) for i in month_range]

    elif int(start_year) < int(end_year):
        year_range = list(range(int(start_year), int(end_year) + 1))
        year_range = ["{0:0=2d}".format(i) for i in year_range]

        if int(start_month) > int(end_month):
            month_range = list(range(int(start_month), 13)) + \
                          list(range(1, int(end_month) + 1))
            month_range = ["{0:0=2d}".format(i) for i in month_range]
            month_range.sort()
        else:
            month_range = list(range(1, 13))
            month_range = ["{0:0=2d}".format(i) for i in month_range]

    return year_range, month_range


def variables_to_download(variables):
    """ Creates two vectors containing information regarding the information that needs to be
    downloaded in order to plot the variables that are desired

    Author: Gorosti Mancho

    Parameters
    ----------
    variables: list of two strings containing the variables of interest


    Returns
    --------
    chosen_variables: list of strings
        List of string containing the variables that need to be downloaded
    regions: list
        List of strings containing the ENSO regions of interest
    """

    chosen_variables = []
    regions = []

    for i in variables:

        if i.split(' ', 1)[0] == 'ENSO':
            regions = regions + [i.split(' ', 1)[1]]

        elif i == 'Energy Budget':
            chosen_variables = chosen_variables + ['surface_latent_heat_flux',
                                                   'surface_net_solar_radiation',
                                                   'surface_net_thermal_radiation',
                                                   'surface_sensible_heat_flux']

        elif i == "Snow Depth":
            chosen_variables = chosen_variables + ['snow_depth',
                                                   'snow_density']

        else:
            chosen_variables.append(plain_text_to_long.get(i))

    return chosen_variables, regions


def clim(filein):
    """Returns monthly climatology for a given region.

    Author: Francesc Roura Adserias

    Parameters
    ----------
    filein: netcdf file
        original monthly sea surface temperature (sst) data for a given region
        and period.

    Returns
    -------
    xarray Dataset
        Sea surface temperature (sst) monthly clmatology.
    """
    # Open data
    data = xr.open_dataset(filein)

    # Check that data exists
    if not os.path.exists(filein):
        raise ValueError("The file" + filein + "does not exist.")

    # Compute regional-monthly mean
    mo_data = data.groupby('time.month').mean()
    mean_data = mo_data.mean(dim=['latitude', 'longitude'])

    return mean_data


def yearly_evol(clim, filein, syear, fyear, smonth, fmonth):
    """Returns monthly anomalies for a given region and a given monthly
    climatology.

    Author: Francesc Roura Adserias

    Parameters
    ----------
    clim: xarray Dataset
        monthly climatology.

    filein: netcdf file
        original monthly-mean data.

    syear: integer
        first year of the period of study.

    smonth: integer
        first month of the period of study.

    fyear: integer
        final year of the period of study.

    fmonth: integer
        last month of the period of study.

    Returns
    -------
    xarray Dataset
        monthly mean sst anomalies during a 12-month period.
    """
    # Check input dates
    if (fyear - syear) > 20:
        raise ValueError(
            "Period of study can not exceed the climatology period"
            " (20 years).")

    if datetime.datetime(syear, smonth, 1) >= datetime.datetime(fyear, fmonth,
                                                                1):
        raise ValueError("Non-consistent start and final dates.")

    data = xr.open_dataset(filein)

    # Spatial mean for the study period
    region_mean = data.mean(dim=['latitude', 'longitude'])
    period = slice(str(syear) + '-' + str(smonth) + '-01',
                   str(fyear) + '-' + str(fmonth) + '-01')

    data_period = region_mean.sst.sel(time=period)

    # Compare climatology to our period.
    npclim = np.array(clim.sst)
    headclim = npclim[(smonth - 1):12]
    if (fyear - syear) == 0:
        midclim = None
    else:
        midclim = np.repeat(npclim, fyear - syear - 1)
    tailclim = npclim[0:fmonth]

    if fyear == syear:  # only one year
        totclim = npclim[(smonth - 1):fmonth]
    else:
        if fmonth == 12:  # last year is complete
            totclim = np.concatenate((headclim, midclim))
        if smonth == 1:  # first year is complete
            totclim = np.concatenate((midclim, tailclim))
        if smonth == 1 & fmonth == 12:
            totclim = midclim
        else:
            totclim = np.concatenate((headclim, midclim, tailclim))

    # Compute anomaly
    ano = data_period - totclim

    return ano
