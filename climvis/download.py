"""
This tool will download the ERA5 data needed to plot the chosen variables

!!Important!!
To run the program without error, check if you have installed all the requirements noted in the README file.
Most importantly you have to have a cdsapi access installed on your computer!
"""
import cdsapi
import warnings


def download_era5(variables, year, month, file):
    """ Download ERA5 data

    Author: Marie Schroeder

    Parameters
    ----------
    variables : list
        A list of the wanted variables to download
    year : list
        A list of the years that should be covered in the dataset
    month : list
        A list of the months that should be covered in the dataset
    file : str
        Path to the data folder with name of the file

    Returns
    -------
    downloads the file requested in data folder
    """

    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'format': 'netcdf',
            'variable': variables,
            'product_type': 'monthly_averaged_reanalysis',
            'year': year,
            'month': month,
            'time': '00:00',
        },
        file)


def dwl_era5_enso(fyear, region, file):
    """Download ERA5 SST data for one of the 4 El Niño regions for the 20
    years before the given year (fyear).

    Author: Francesc Roura Adserias

    Parameters
    ----------
    fyear : integer
        last year of the 20-year period.
    region : string
        String indicating the "el niño" region.
        It must be "en12" (El niño 1+2),"en3" (El niño 3),"en34" (El niño 3.4),
        or "en4" (El niño 4).
    file : str
        Path to the data folder with name of the file

    Returns
    -------
    Downloads the requested files in data folder
    """
    if int(fyear) > 2019 or int(fyear) < 1979:
        raise ValueError('Final year must be in the 1979-2019 period.')

    c = cdsapi.Client()

    # To be faster, resolution is reduced
    grid = [1, 1]

    # el niño 1+2
    if region == "en12":
        area = [0, -90, -10, -80]
    # el niño 3
    elif region == "en3":
        area = [5, -150, -5, -90]
    # el niño 3.4
    elif region == "en34":
        area = [5, -170, -5, -120]
    # el niño 3.4
    elif region == "en4":
        area = [5, 160, -5, -150]
    else:
        raise ValueError('Arg "region" must be: "en12","en3","en34" or "en4".')

    # 20-year period, monthly data
    if int(fyear) - 20 < 1979:  # no data before 1979
        year = ['{}'.format(y) for y in range(int(fyear) - 20,
                                              int(
                                                  int(fyear) + int(fyear) + 20 - 1979) + 1)]
        warnings.warn("Climatology computed from 1979 to 1999.")
    else:
        year = ['{}'.format(y) for y in range(int(fyear) - 20, int(fyear) + 1)]

    # All months
    month = ['{:02d}'.format(m) for m in range(1, 13)]

    c.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'format': 'netcdf',
            'product_type': 'monthly_averaged_reanalysis',
            'variable': [
                'sea_surface_temperature',
            ],
            'grid': grid,
            'area': area,
            'year': year,
            'month': month,
            'time': '00:00'
        },
        file)
