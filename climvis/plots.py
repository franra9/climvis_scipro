"""
In this file all the functions for making the final plot in the interface are stored.
"""

import xarray as xr
from climvis.functions import clim, yearly_evol, path
from scipy import stats
import os

# path to data folder
file_dir = path()

long_name_to_short_name = {
    "2m_temperature": "t2m",
    "surface_latent_heat_flux": "slhf",
    "surface_sensible_heat_flux": "sshf",
    "surface_net_solar_radiation": "ssr",
    "surface_net_thermal_radiation": "str",
    "snow_depth": "sd",
    "snow_density": "rsn",
    "lake_cover": "cl",
    "friction_velocity": "zust",
    "cloud_base_height": "cbh",
    "snow_albedo": "asn",
    "sea_surface_temperature": "sst",
    "surface_pressure": "sp",
    "soil_temperature_level_1": "stl1",
    "boundary_layer_height": "blh",
    "low_cloud_cover": "lcc",
    "medium_cloud_cover": "mcc",
    "high_cloud_cover": "hcc"
}

plain_text_to_long = {
    "Temperature at 2m": "2m_temperature",
    "Lake Cover": "lake_cover",
    "Friction Velocity": "friction_velocity",
    "Cloud Base Height": "cloud_base_height",
    "Snow Albedo": "snow_albedo",
    "Sea Surface Temperature": "sea_surface_temperature",
    "Surface Pressure": "surface_pressure",
    "Soil Temperature": "soil_temperature_level_1",
    "Boundary Layer Height": "boundary_layer_height",
    "Low Cloud Cover": "low_cloud_cover",
    "Medium Cloud Cover": "medium_cloud_cover",
    "High Cloud Cover": "high_cloud_cover"
}

long_name_to_units = {
    "2m_temperature": "[K]",
    "lake_cover": "[]",
    "friction_velocity": "[m/s]",
    "cloud_base_height": "[m]",
    "snow_albedo": "[m]",
    "sea_surface_temperature": "[K]",
    "surface_pressure": "[Pa]",
    "soil_temperature_level_1": "[K]",
    "boundary_layer_height": "[m]",
    "low_cloud_cover": "[0-1]",
    "medium_cloud_cover": "[0-1]",
    "high_cloud_cover": "[0-1]"
}

enso_to_full_name = {
    "ENSO en12": "ENSO Region 1+2",
    "ENSO en3": "ENSO Region 3",
    "ENSO en34": "ENSO Region 3.4",
    "ENSO en4": "ENSO Region 4"
                ""
}
"ENSO en12", "ENSO en3", "ENSO en34", "ENSO en4"


def plot_snow(data, ax, long, lat, location, start, end):
    """Calculates the snow depth in meter and plots it

    Author: Marie Schroeder

    Parameters
    ----------
    data: netCDF file
        file that has been downloaded with ERA5 data
    ax: axes
        axes on which the plot will be made
    long: float
        longitude
    lat: float
        latitude
    location: str
        location of the legend
    start: str
        the start date in format yyyy-mm-dd
    end: str
        the end date in format yyyy-mm-dd

    Returns
    -------
    sd:
    """
    # snow depth in water equivalent
    sd_we = data.sd.sel(longitude=long, latitude=lat, time=slice(start, end))

    # snow depth in meter
    snow_density = data.rsn.sel(longitude=long, latitude=lat, time=slice(start, end))
    water_density = 1000  # kg m^-3
    sd = water_density * sd_we / snow_density

    ax.plot(sd.time, sd, color="deepskyblue")
    ax.legend(["Snow Depth"], loc=location)
    ax.set_ylabel("Snow Depth (m)")

    return sd, ax


def plot_fluxes(data, ax, long, lat, location, start, end):
    latent = data.slhf.sel(longitude=long, latitude=lat, time=slice(start, end))
    sensible = data.sshf.sel(longitude=long, latitude=lat, time=slice(start, end))
    sw_net = data.ssr.sel(longitude=long, latitude=lat, time=slice(start, end))
    lw_net = data.str.sel(longitude=long, latitude=lat, time=slice(start, end))

    ax.plot(sw_net.time, sw_net / 86400, "m")
    ax.plot(sw_net.time, lw_net / 86400, "royalblue")
    ax.plot(sw_net.time, latent / 86400, "g")
    ax.plot(sw_net.time, sensible / 86400, "orange")
    ax.legend(["SW_net", "LW_net", "Latent Heat Flux", "Sensible Heat Flux"], loc=location)
    ax.set_ylabel("Energy Fluxes (W m^2)")

    return latent, ax


def plot_enso(data, ax, variable_name, color, location):
    ax.plot(data.time, data, color)

    ax.set_ylabel('El Nino Index')
    ax.legend([enso_to_full_name.get(variable_name)], loc=location)


def plot_any_variable(data, ax, long, lat, variable_name, color, location, start, end):
    long_name = plain_text_to_long.get(variable_name)
    short_name = long_name_to_short_name.get(long_name)
    units = long_name_to_units.get(long_name)
    variable_data = data[short_name].sel(longitude=long, latitude=lat, time=slice(start, end))

    if units == "[K]":
        ax.plot(variable_data.time, variable_data - 273.15, color)
        ax.set_ylabel(variable_name + " [°C]")

    else:
        ax.plot(variable_data.time, variable_data, color)
        ax.set_ylabel(variable_name + " " + units)

    ax.legend([variable_name], loc=location)

    return variable_data, ax


def final_plot(date, variable, figure, long, lat, file):
    """Makes a plot of the chosen variable for a given longitude and latitude

    Parameters
    ----------
    date: list
        A list of the start year, end year, start month and end month
    variable: list
        A list with the 2 variable names inside
    figure: fig
        The figure in the tkinter interface, where the plot will be shown
    long: float
        The longitude
    lat: float
        The latitude
    file: str
        path to the file with the ERA5 data from all the variables except El Nino

    Returns
    -------
    Plot
    """
    if os.path.exists(file):
        data = xr.open_dataset(file)
    ax = figure.subplots(1)
    ax2 = ax.twinx()
    ano = [None] * 2

    axis = [ax, ax2]
    series = [None] * 2
    Color = ['b', 'r']
    location = ['upper left', 'upper right']

    start_date = date[0] + "-" + "{0:0=2d}".format(int(date[2])) + "-01"
    end_date = date[1] + "-" + "{0:0=2d}".format(int(date[3])) + "-01"

    for i in range(0, 2):

        if variable[i] == "Energy Budget":
            series[i], ax_test = plot_fluxes(data, axis[i], long, lat, location[i], start_date, end_date)

        elif variable[i] == "Snow Depth":
            series[i], ax_test = plot_snow(data, axis[i], long, lat, location[i], start_date, end_date)

        elif variable[i].split(' ', 1)[0] == 'ENSO':

            date = list(map(int, date))
            region = variable[i].split(' ', 1)[1]
            filein = os.path.join(file_dir, 'ERA5_Monthly_sst_' + str(date[1]) + '_' + region + '.nc')
            climate = clim(filein)
            ano[i] = yearly_evol(climate, filein, date[0], date[1], date[2], date[3])
            series[i] = ano[i]

            plot_enso(ano[i], axis[i], variable[i], Color[i], location[i])

        else:
            series[i], ax_test = plot_any_variable(data, axis[i], long, lat, variable[i], Color[i], location[i],
                                                   start_date,
                                                   end_date)

        ymin, ymax = axis[i].get_ylim()
        axis[i].set_ylim(ymin, ymin + (ymax - ymin) * 1.2)

    ax.set_xlabel("Time")
    ax.set_title(variable[0] + " vs " + variable[1] +
                 " at Longitude = {}º and Latitude = {}º".format(long - 180, lat))
    ax.set_xlim(start_date, end_date)

    figure.tight_layout()
    figure.autofmt_xdate()

    correlation = stats.pearsonr(series[0], series[1])

    return correlation[0], ax
