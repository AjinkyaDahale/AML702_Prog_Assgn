#!/usr/bin/python3

import sys, traceback

from gi.repository import Gtk

from matplotlib.figure import Figure
from numpy import sin, cos, pi, linspace, log, exp, floor, piecewise
#Possibly this rendering backend is broken currently
#from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

from guisetup import MethodDetailsBox

class MainClass():
    def __init__(self):
        # Gets all the objects of interest: windows, list boxes, graphviews etc
        self.builder = Gtk.Builder()
        self.builder.add_from_file('gui/igl-app-window-2.glade')
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('window1')

        self.sw = self.builder.get_object('graphscrollwindow')
        self.sw2 = self.builder.get_object('graphtools')

        self.gtbrevealer = self.builder.get_object('graphtoolsrevealer')
        self.m1revealer = self.builder.get_object('method1revealer')
        self.m2revealer = self.builder.get_object('method2revealer')

        self.fnbox = self.builder.get_object('functioncbtext')
        self.aentry = self.builder.get_object('aentry')
        self.bentry = self.builder.get_object('bentry')

        # Use Headerbar for inputs

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.set_custom_title(self.builder.get_object('titlebox'))

        self.window.set_titlebar(self.hb)

        # Adds widgets that change the view as per method

        self.m1box = MethodDetailsBox()
        self.m2box = MethodDetailsBox()
        self.m1revealer.add(self.m1box)
        self.m2revealer.add(self.m2box)
        
        # TODO: Plot as per the defaults to get started

        self.fig = Figure(figsize=(5,5), dpi=80)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.sw.add_with_viewport(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self.window)
        self.sw2.add_with_viewport(self.toolbar)

        self.on_params_changed(None)

    def on_window1_destroy(self, widget):
        Gtk.main_quit()

    def toggle_allreveal(self, widget):
        self.toggle_m1reveal(widget)
        self.toggle_m2reveal(widget)
        self.toggle_gtbreveal(widget)

    # TODO make these change as per the toggle, rather than simply toggling

    def toggle_gtbreveal(self, widget):
        if self.gtbrevealer.get_reveal_child():
            self.gtbrevealer.set_reveal_child(False)
        else:
            self.gtbrevealer.set_reveal_child(True)

    def toggle_m1reveal(self, widget):
        if self.m1revealer.get_reveal_child():
            self.m1revealer.set_reveal_child(False)
        else:
            self.m1revealer.set_reveal_child(True)
            
    def toggle_m2reveal(self, widget):
        if self.m2revealer.get_reveal_child():
            self.m2revealer.set_reveal_child(False)
        else:
            self.m2revealer.set_reveal_child(True)

    def resetplot(self):
        self.ax.cla()
        self.ax.grid(True)

    def plotexact(self):
        self.resetplot()
        n = 1000
        xs = linspace(self.a, self.b, n, endpoint=True)
        fxs = self.f(xs)
        fxexact = self.ax.plot(xs, fxs, color='black', label='f(x)')

    def plotapprox(self):
        pass
#        fxapprox1 = self.ax.plot(xs, self.m1box.fapprox(xs), color='blue', label='Method 1')
#        fxapprox2 = self.ax.plot(xs, self.m2box.fapprox(xs), color='red', label='Method 1')

    def on_params_changed(self, widget):
        # print 'Integrand changed'
        try:
            self.f = eval('lambda x: '+self.fnbox.get_active_text())
            self.a = eval(self.aentry.get_text())
            self.b = eval(self.bentry.get_text())
            self.plotexact()
            self.m1box.set_exact_function_and_bounds(self.f,self.a,self.b)
            self.m2box.set_exact_function_and_bounds(self.f,self.a,self.b)
        except:
            traceback.print_exc()
        finally:
            self.canvas.draw()

mc = MainClass()

mc.window.connect("delete-event", Gtk.main_quit)
mc.window.show_all()
Gtk.main()
