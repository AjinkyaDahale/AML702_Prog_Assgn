#!/usr/bin/python3

from gi.repository import Gtk

from matplotlib.figure import Figure
from numpy import sin, cos, pi, linspace
#Possibly this rendering backend is broken currently
#from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

class Signals:
    def on_window1_destroy(self, widget):
        Gtk.main_quit()

    def toggle_allreveal(self, widget):
        self.toggle_m1reveal(widget)
        self.toggle_m2reveal(widget)
        self.toggle_gtbreveal(widget)

    def toggle_gtbreveal(self, widget):
        if gtbrevealer.get_reveal_child():
            gtbrevealer.set_reveal_child(False)
        else:
            gtbrevealer.set_reveal_child(True)
              
    def toggle_m1reveal(self, widget):
        if m1revealer.get_reveal_child():
            m1revealer.set_reveal_child(False)
        else:
            m1revealer.set_reveal_child(True)
            
    def toggle_m2reveal(self, widget):
        if m2revealer.get_reveal_child():
            m2revealer.set_reveal_child(False)
        else:
            m2revealer.set_reveal_child(True)

builder = Gtk.Builder()
builder.add_objects_from_file('gui/igl-app-window.glade', ('window1', '') )
builder.connect_signals(Signals())

myfirstwindow = builder.get_object('window1')
sw = builder.get_object('graphscrollwindow')
sw2 = builder.get_object('graphtools')

gtbrevealer = builder.get_object('graphtoolsrevealer')
m1revealer = builder.get_object('method1revealer')
m2revealer = builder.get_object('method2revealer')

myfirstwindow.show_all()
Gtk.main()
