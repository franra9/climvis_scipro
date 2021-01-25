"""The main program from where the interface will open, with all the necessary
functions for the interface to run  """

import tkinter as tk
import cartopy.crs as ccrs  # Projections list
import cartopy.feature as cfeature
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from climvis.functions import era5_pos, process_date, variables_to_download, \
    path
from climvis.download import download_era5, dwl_era5_enso
import os
import climvis.plots as plots
import sys

matplotlib.use('TkAgg')

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

# open tkinter window in which the whole application will run
root = tk.Tk()
root.title('ERA5 Visualization App')
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
root.geometry(f"{screen_width}x{screen_height}")

# empty figure in the window that shows where the final plot will be displayed
fig = plt.figure(figsize=(8, 6))
text = fig.text(.4, .75, "Your plot will be shown here")
# embedding the plot in the tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(column=4, row=1, rowspan=10, columnspan=10)

# second Canva to show the El Nino regions if they are chosen
canvas_2 = tk.Canvas(root, width=300, height=92)
canvas_2.grid(column=8, row=11, columnspan=8, rowspan=4)

# path to data folder
file_dir = path()

# Part 1: Choosing a start date and end date
global start_year, start_month, end_year, end_month
start_year, start_month, end_year, end_month = "", "", "", ""


def grab_start_date():
    """Saves start date

    Author: Marie Schroeder

    Returns
    -------
    start_month : str
        The start month the user chose
    start_year : str
        The start year the user chose
    """
    start_date_label.config(text=clicked_start_month.get() + "/" +
                                 clicked_start_year.get())
    global start_year, start_month
    start_month = clicked_start_month.get()
    start_year = clicked_start_year.get()
    # show download button if all variables (start_date, end_date, position,
    # variables) got chosen
    if start_year and start_month and end_year and end_month and lon and lat \
            and var[0] and var[1]:
        download_button.grid(column=0, row=14)


def grab_end_date():
    """Saves end date

    Author: Marie Schroeder

    Returns
    -------
    end_month : str
        The end month the user chose
    end_year : str
        The end year the user chose
    """
    end_date_label.config(text=clicked_end_month.get() + "/" +
                               clicked_end_year.get())
    global end_year, end_month
    end_month = clicked_end_month.get()
    end_year = clicked_end_year.get()
    if int(end_year) < int(start_year) or \
            (int(start_year) == int(end_year) and
             int(end_month) < int(start_month)):
        end_date_label.config(text="Your end date must be "
                                   "after the start date!")
    # show download button if all variables (start_date, end_date,
    # position, variables) got chosen
    if start_year and start_month and end_year and end_month and lon and lat \
            and var[0] and var[1]:
        download_button.grid(column=0, row=14)


# Dropdown menu for the user to choose start year and month
clicked_start_month = tk.StringVar()
clicked_start_month.set("Choose Month")

drop_start_month = tk.OptionMenu(root, clicked_start_month,
                                 *list(range(1, 13)))
drop_start_month.grid(column=0, row=1)
drop_start_month.config(font="Ariel")
menu_start_month = root.nametowidget(drop_start_month.menuname)
menu_start_month.config(font="Ariel")

clicked_start_year = tk.StringVar()
clicked_start_year.set("Choose Year")

drop_start_year = tk.OptionMenu(root, clicked_start_year,
                                *list(range(1979, 2020)))
drop_start_year.grid(column=0, row=2)
drop_start_year.config(font="Ariel")
menu_start_year = root.nametowidget(drop_start_year.menuname)
menu_start_year.config(font="Ariel")

# Dropdown menu for the user to choose end year and month
clicked_end_month = tk.StringVar()
clicked_end_month.set("Choose Month")

drop_end_month = tk.OptionMenu(root, clicked_end_month, *list(range(1, 13)))
drop_end_month.grid(column=1, row=1)
drop_end_month.config(font="Ariel")
menu_end_month = root.nametowidget(drop_end_month.menuname)
menu_end_month.config(font="Ariel")

clicked_end_year = tk.StringVar()
clicked_end_year.set("Choose Year")

drop_end_year = tk.OptionMenu(root, clicked_end_year, *list(range(1979, 2020)))
drop_end_year.grid(column=1, row=2)
drop_end_year.config(font="Ariel")
menu_end_year = root.nametowidget(drop_end_year.menuname)
menu_end_year.config(font="Ariel")

# Part 2: Choosing a location

global lon, lat
lon, lat = float(), float()


def interactive_map():
    """Opens an interactive map from which the user can choose a location

    Author: Marie Schroeder

    Returns
    -------
    lon : float
        The chosen longitude
    lat : float
        The chosen latitude
    """
    fig1, ax = plt.subplots()
    ax = plt.axes(projection=ccrs.PlateCarree())
    plt.figtext(.5, .93, 'Click anywhere on the map to choose '
                         'the location of interest', fontsize=14, ha='center')
    plt.figtext(.5, .9, '(in the top right corner you can see the '
                        'coordinates of the location of your mouse)',
                fontsize=8, ha='center')
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)

    def onclick(event):
        """Written by: Marie Schroeder
        Saves the x and y component when clicking on a map

        Parameters
        ----------
        event: click event
            gets the x and y component when clicking on a map

        Returns
        -------
        lon: float
            longitude
        lat: float
            latitude
        """
        global lon, lat
        x_data = event.xdata
        y_data = event.ydata

        if x_data and y_data:
            fig1.canvas.mpl_disconnect(cid)
            plt.close()
            lon, lat = era5_pos(x_data, y_data)
            location_label.config(text="Longitude: " + str(lon - 180)
                                       + "\nLatitude: " + str(lat))
            # show download button if all variables
            # (start_date, end_date, position, variables) got chosen
            if start_year and start_month and end_year and end_month and \
                    lon and lat and var[0] and var[1]:
                download_button.grid(column=0, row=14)

    cid = fig1.canvas.mpl_connect('button_press_event', onclick)
    fig1.show()


# Part 3: Choosing 2 variables to compare
global var
var = [None] * 2


def select_variable_1():
    """Saves the 1st variable the user chooses

    Author: Marie Schroeder and Gorosti Mancho

    Returns
    --------
    variable_1 : str
        The variable the user chose
    chosen_variables : list
        A list with the 2 variables
    """
    global var
    var[0] = clicked_var_1.get()
    variable_label_1.config(text=var[0])
    # show download button if all variables
    # (start_date, end_date, position, variables) got chosen
    if start_year and start_month and end_year and end_month and \
            lon and lat and var[0] and var[1]:
        download_button.grid(column=0, row=14)


def select_variable_2():
    """Saves the 2nd variable the user chooses

    Author: Marie Schroeder and Gorosti Mancho

    Returns
    --------
    variable_2 : str
        The variable the user chose
    chosen_variables : list
        A list with the 2 variables
    """
    global var
    var[1] = clicked_var_2.get()
    variable_label_2.config(text=var[1])
    # show download button if all variables
    # (start_date, end_date, position, variables) got chosen
    if start_year and start_month and end_year and end_month and \
            lon and lat and var[0] and var[1]:
        download_button.grid(column=0, row=14)


# Dropdown menu for the user to choose 1st variable
variables = ["Energy Budget", "Snow Depth",
             "ENSO en12", "ENSO en3", "ENSO en34", "ENSO en4"]
variables.extend(list(plain_text_to_long.keys()))

clicked_var_1 = tk.StringVar()
clicked_var_1.set("Choose variable 1")

drop_var_1 = tk.OptionMenu(root, clicked_var_1, *variables)
drop_var_1.grid(column=0, row=9)
drop_var_1.config(font="Ariel")
menu_var_1 = root.nametowidget(drop_var_1.menuname)
menu_var_1.config(font="Ariel")

# Dropdown menu for the user to choose 2nd variable

clicked_var_2 = tk.StringVar()
clicked_var_2.set("Choose variable 2")

drop_var_2 = tk.OptionMenu(root, clicked_var_2, *variables)
drop_var_2.grid(column=0, row=11)
drop_var_2.config(font="Ariel")
menu_var_2 = root.nametowidget(drop_var_2.menuname)
menu_var_2.config(font="Ariel")


# Part 4: Downloading the corresponding data

def download_button():
    """Downloads the file needed from ERA5 server given the variables
     and dates the user chose

    Author: Marie Schroeder and Gorosti Mancho

    Returns
    -------
    Downloaded file in working directory
    """
    year_range, month_range = process_date(start_year, start_month,
                                           end_year, end_month)
    chosen_variables, regions = variables_to_download(var)
    print(regions)

    answer = tk.messagebox.askquestion("Download",
                                       "Do you want to start the download "
                                       "now?")
    if answer == "yes":
        if chosen_variables:
            # noinspection LongLine
            if os.path.exists(os.path.join(file_dir, "era5_data.nc")):
                answer2 = tk.messagebox.askquestion("File already exists!",
                                                    "Attention! A file with "
                                                    "the same name as the "
                                                    "downloaded one already"
                                                    " exist."
                                                    "\nIf you continue it will"
                                                    " be overwritten with the "
                                                    "new file."
                                                    "\nDo you want to "
                                                    "continue?",
                                                    icon="warning")

                if answer2 == "yes":
                    tk.messagebox.showinfo("Explanation", "The download"
                                                          " will start now."
                                                          "\nJust wait until"
                                                          " you see 'Your File"
                                                          " is downloaded!' "
                                                          "on the screen "
                                                          "\nYou can see the "
                                                          "progress of the"
                                                          " download in the"
                                                          " command line.")

                    download_era5(chosen_variables, year_range, month_range,
                                  os.path.join(file_dir, 'era5_data.nc'))

                    if os.path.exists(os.path.join(file_dir, 'era5_data.nc')):
                        download_update.config(text="Your file is downloaded!")
                        # show the button to plot your data as soon as
                        # the file exists in the directory
                        accept_button = tk.Button(root, text='Make Plot',
                                                  command=plot_result,
                                                  font=("Ariel", 20, "bold"),
                                                  bg='red', fg='white')
                        accept_button.grid(column=1, row=14)

            else:
                tk.messagebox.showinfo("Explanation", "The download "
                                                      "will start now."
                                                      "\nJust wait until you"
                                                      " see 'Your File "
                                                      "is downloaded!' "
                                                      "on the screen"
                                                      "\nYou can see the "
                                                      "progress of the "
                                                      "download in the "
                                                      "command line.")

                download_era5(chosen_variables, year_range, month_range,
                              os.path.join(file_dir, 'era5_data.nc'))

                if os.path.exists(os.path.join(file_dir, 'era5_data.nc')):
                    download_update.config(text="Your file is downloaded!")
                    # show the button to plot your data as soon as
                    # the file exists in the directory
                    accept_button = tk.Button(root, text='Make Plot',
                                              command=plot_result,
                                              font=("Ariel", 20, "bold"),
                                              bg='red', fg='white')
                    accept_button.grid(column=1, row=14)

        if regions:
            for i in regions:
                dwl_era5_enso(end_year, i,
                              os.path.join(file_dir, 'ERA5_Monthly_sst_' +
                                           str(end_year) + '_' + i + '.nc'))

            accept_button = tk.Button(root, text='Make Plot',
                                      command=plot_result,
                                      font=("Ariel", 20, "bold"),
                                      bg='red', fg='white')
            accept_button.grid(column=1, row=14)


# Part 5: Making the plot of all the chosen options
nino_png = os.path.join(file_dir, "nino.png")
img = tk.PhotoImage(file=nino_png)


def plot_result():
    """Makes a plot with the 2 chosen variables

    Author: Marie Schroeder and Gorosti Mancho

    Returns
    -------
    Plot
    """
    text.set_visible(False)
    date = [start_year, end_year, start_month, end_month]
    correlation, ax = plots.final_plot(date, var, fig, lon, lat,
                                       os.path.join(file_dir, 'era5_data.nc'))

    # embedding figure in tkinter window
    canvas_3 = FigureCanvasTkAgg(fig, master=root)
    canvas_3.draw()
    canvas_3.get_tk_widget().grid(column=4, row=1, rowspan=10, columnspan=10)

    # adding the matplotlib toolbar
    toolbarFrame = tk.Frame(master=root)
    toolbarFrame.grid(row=10, column=7)
    NavigationToolbar2Tk(canvas, toolbarFrame)

    correlation_label.config(text='The correlation between '
                                  'the two variables is: '
                                  + str(round(correlation, 2)))

    # adding a ENSO region image for overview if ENSO is chosen as a variable
    # noinspection PyUnresolvedReferences
    if "ENSO" in {var[0].split()[0], var[1].split()[0]}:
        canvas_2.create_image(0, 0, anchor='nw', image=img)


# An empty column between the figure and the buttons
empty_space = tk.Label(root, text='', width=10)
empty_space.grid(column=3, row=2)

# Part 6: All the Buttons and Labels that are needed for the interface
# Buttons and Labels for the user to choose the start and end date

some_text = tk.Label(root, text='Choose the date range of interest:',
                     font="Ariel", fg="Steel Blue")
some_text.grid(column=0, row=0, sticky="W")

start_date_button = tk.Button(root, text='Select Start Date',
                              command=grab_start_date, font="Ariel")
start_date_button.grid(column=0, row=3)

start_date_label = tk.Label(root, text='', font="Ariel")
start_date_label.grid(column=0, row=4)

end_date_button = tk.Button(root, text='Select End Date',
                            command=grab_end_date, font="Ariel")
end_date_button.grid(column=1, row=3)

end_date_label = tk.Label(root, text='', font="Ariel")
end_date_label.grid(column=1, row=4)

# Button and Labels for the user to choose the location
some_text_4 = tk.Label(root, text="Choose Location of interest",
                       font="Ariel", fg="Steel Blue")
some_text_4.grid(column=0, row=5, sticky="W")

some_text_5 = tk.Label(root, text="Click the button and choose "
                                  "your location of \ninterest "
                                  "by clicking on the map",
                       font="Ariel")
some_text_5.grid(column=0, row=6)

location_button = tk.Button(root, text="Choose Location",
                            command=interactive_map, font="Ariel")
location_button.grid(column=1, row=6)

location_label = tk.Label(root, text='', font="Ariel")
location_label.grid(column=1, row=7)

# Buttons and labels for the user to choose the 2 variables
some_text_6 = tk.Label(root, text="Choose 2 variables to compare",
                       font="Ariel", fg="Steel Blue")
some_text_6.grid(column=0, row=8, sticky="W")

variable_button_1 = tk.Button(root, text="Select Variable 1",
                              command=select_variable_1, font="Ariel")
variable_button_1.grid(column=1, row=9)

variable_label_1 = tk.Label(root, text='', font="Ariel")
variable_label_1.grid(column=1, row=10)

variable_button_2 = tk.Button(root, text="Select Variable 2",
                              command=select_variable_2, font="Ariel")
variable_button_2.grid(column=1, row=11)

variable_label_2 = tk.Label(root, text='', font="Ariel")
variable_label_2.grid(column=1, row=12)

# Button to start the download
download_button = tk.Button(root, text="Download", command=download_button,
                            font=("Ariel", 20, "bold"), bg='blue',
                            fg='white')
download_button.grid(column=0, row=14)
download_button.grid_remove()

download_update = tk.Label(root, text='', font="Ariel")
download_update.grid(column=1, row=13)

# Label to display the correlation between the two variables
correlation_label = tk.Label(root, text='', font="Ariel")
correlation_label.grid(column=4, row=13, columnspan=4)


# ask user before closing the interface window


def on_closing():
    """Stops the program when the 'x' button in the upper right corner is clicked
    and gives a warning before closing

    Author: Marie Schroeder
    """
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
