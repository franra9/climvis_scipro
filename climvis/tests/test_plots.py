"""Test file for all the functions in plots.py"""

from climvis.plots import plot_snow, plot_fluxes, final_plot, plot_any_variable
from climvis.functions import path
import matplotlib.pyplot as plt
import xarray as xr
import os

start_date = "2017-03-01"
end_date = "2018-02-01"

# path to data folder
file_dir = path()

def test_plot_snow():
    # Author: Marie Schroeder
    fig, ax = plt.subplots()
    data = xr.open_dataset(os.path.join(file_dir, "data_for_tests.nc"))
    not_important, ax_test = plot_snow(data, ax, 45, 11, "upper right", start_date, end_date)

    # Check if something got plotted
    assert ax_test.lines != []

    # Check if axes get labeled
    assert ax_test.get_ylabel() == "Snow Depth (m)"

    # Check if legend is plotted
    assert ax_test.get_legend() is not None


def test_plot_fluxes():
    # Author: Marie Schroeder
    fig, ax = plt.subplots()
    data = xr.open_dataset(os.path.join(file_dir, "data_for_tests.nc"))
    not_important, ax_test = plot_fluxes(data, ax, 45, 11, "upper right", start_date, end_date)

    # Check if something got plotted
    assert ax_test.lines != []

    # Check if axes get labeled
    assert ax_test.get_ylabel() == "Energy Fluxes (W m^2)"

    # Check if legend is plotted
    assert ax_test.get_legend() is not None


def test_final_plot():
    # Author: Marie Schroeder
    fig = plt.figure()
    not_important, ax = final_plot(["2017", "2018", "03", "02"], ["Energy Budget", "Temperature at 2m"], fig, 45, 11, os.path.join(file_dir, "data_for_tests.nc"))

    # Check if the title is displayed in the figure
    ref = "Energy Budget vs Temperature at 2m at Longitude = -135º and Latitude = 11º"
    assert ref == ax.get_title()

    # Check if something got plotted
    assert ax.lines != []


def test_plot_any_variable():
    # Author: Gorosti Mancho
    fig, ax = plt.subplots()
    data = xr.open_dataset(os.path.join(file_dir, "data_for_tests.nc"))
    not_important, ax_test = plot_any_variable(data, ax, 45, 11, 'Medium Cloud Cover', 'r', 'upper right', start_date,
                                               end_date)

    # Check if something got plotted
    assert ax_test.lines != []

    # Check if axes get labeled
    assert ax_test.get_ylabel() == "Medium Cloud Cover [0-1]"

    # Check if legend is plotted
    assert ax_test.get_legend() is not None
