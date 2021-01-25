"""Test file for all the functions in main.py"""

from climvis.main import era5vis_io
import climvis


def test_era5vis_io(capsys):
    # Author: Marie Schroeder
    # test if help opens if no arguments are put in
    era5vis_io([])
    captured = capsys.readouterr()
    assert 'Usage:' in captured.out

    # test if help opens if -h or --help is typed
    era5vis_io(["-h"])
    captured = capsys.readouterr()
    assert 'Usage:' in captured.out

    era5vis_io(["--help"])
    captured = capsys.readouterr()
    assert 'Usage:' in captured.out

    # test if version opens if -v or --version is typed
    era5vis_io(['-v'])
    captured = capsys.readouterr()
    assert climvis.__version__ in captured.out

    # test -s and --start statements with too many arguments
    era5vis_io(['-s', 3])
    captured = capsys.readouterr()
    assert 'era5vis doesnt need any commandline arguments just type: ' \
           'era5vis -s' in captured.out
