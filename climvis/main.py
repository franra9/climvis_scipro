"""Main file from where the program will start when you call era5vis in
the command line"""
import sys
import climvis
import os

HELP = """era5vis: ERA5 variable comparison interactive tool

Usage:
   -h, --help            : print the help
   -v, --version         : print the installed version
   -s, --start           : start interactive program

If you need further instructions to use the interactive panel, look into 
the README file.
"""


# noinspection PyStatementEffect
def era5vis_io(args):
    """Written by: Marie Schroeder
    Different command line arguments for era5vis

    Parameters
    ----------
    args: list
        list of command line input arguments that describes what should happen

    Returns
    -------
    Depending on the argument it opens the help, shows the version or opens
    the interface
    """
    if len(args) == 0:
        print(HELP)
    elif args[0] in ['-h', '--help']:
        print(HELP)
    elif args[0] in ['-v', '--version']:
        print('era5vis: ' + climvis.__version__)
        print('License: public domain')
        print('era5vis is provided "as is", without warranty of any kind')
    elif args[0] in ['-s', '--start']:
        # creating a file called .era5vis with the path to the
        # data_for_tests.nc file to run the tests
        home = os.path.expanduser("~")
        file_name = ".era5vis"
        file_path = os.path.join(home, file_name)

        if not os.path.exists(file_path):
            era5_dir = input("Please enter the path to the folder "
                             "called 'data' (in the package under "
                             "climvis_scipro/climvis/data):")
            era5_test_file = os.path.join(os.path.realpath(era5_dir), 'data_for_tests.nc')
            png_file = os.path.join(os.path.realpath(era5_dir), 'nino.png')

            if os.path.exists(era5_test_file) and os.path.exists(png_file):
                file = open(file_path, "w")
                file.write(os.path.realpath(era5_dir))
                file.close()
            else:
                print("The path to the CRU data you entered is not working. "
                      "Please enter a valid path.")

        if len(args) > 1:
            print('era5vis doesnt need any commandline arguments just type: '
                  'era5vis -s')
            return
        else:
            print('The interface window has opened!')
            import climvis.interface as interface
            interface

    else:
        print('era5vis: command not understood. '
              'Type "era5vis --help" for usage options.')


def era5vis():
    """Entry point for the era5vis application script"""

    era5vis_io(sys.argv[1:])
