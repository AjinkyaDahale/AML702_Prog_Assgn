from gi.repository import Gtk

from matplotlib.figure import Figure
from numpy import sin, cos, pi, linspace, log
#Possibly this rendering backend is broken currently
#from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

class IglDemoWindow(Gtk.Window):
    def __init__(self):
        ''' Sets the window, its headerbar, and whatever else is needed.'''
        pass

    def refresh_plot(self):
        ''' Refreshes the plot. Separated from the updates of the widgets.'''
        pass

    def update_results(self):
        ''' TODO: Changes the widgets related to the methods. Shows the results from each method below it, and issues to update the plot.'''
        pass
