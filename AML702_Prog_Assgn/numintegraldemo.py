#!/usr/bin/python3

from gi.repository import Gtk

from matplotlib.figure import Figure
from numpy import sin, cos, pi, linspace, log
#Possibly this rendering backend is broken currently
#from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

# Signals ----------------------------------------------------------------------
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

    # TODO make these change as per the toggle, rather than simply toggling

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

# Gets all the objects of interest: windows, list boxes, graphviews etc
builder = Gtk.Builder()
builder.add_objects_from_file('gui/igl-app-window.glade', ('window1', '') )
builder.add_objects_from_file('gui/igl-app-window.glade', ('titlebox', '') )
builder.connect_signals(Signals())

myfirstwindow = builder.get_object('window1')
sw = builder.get_object('graphscrollwindow')
sw2 = builder.get_object('graphtools')

gtbrevealer = builder.get_object('graphtoolsrevealer')
m1revealer = builder.get_object('method1revealer')
m2revealer = builder.get_object('method2revealer')

# Use Headerbar for inputs

hb = Gtk.HeaderBar()
hb.set_show_close_button(True)
hb.set_custom_title(builder.get_object('titlebox'))

myfirstwindow.set_titlebar(hb)

# TODO: Replace all this mess by code for exact solution and the 2 methods to compare.

fig = Figure(figsize=(5,5), dpi=80)
ax = fig.add_subplot(111)

f = lambda x: sin(14+x)

n = 1000
xs = linspace(-pi, pi, n, endpoint=True)
# xcos = linspace(-pi, pi, n, endpoint=True)
fxs = f(xs)
# ycos = cos(xcos)

fxexact = ax.plot(xs, fxs, color='black', label='f(x)')
m1approx = ax.plot(xs[::100], fxs[::100], color='black', label='Approx 1', linestyle='--')

ax.set_xlim(-pi,pi)
ax.set_ylim(min(fxs),max(fxs))

# ax.fill_between(xs, 0, fxs, (fxs - 1) > -1, color='blue', alpha=.3)
# ax.fill_between(xs, 0, fxs, (fxs - 1) < -1, color='red',  alpha=.3)
# ax.fill_between(xcos, 0, ycos, (ycos - 1) > -1, color='blue', alpha=.3)
# ax.fill_between(xcos, 0, ycos, (ycos - 1) < -1, color='red',  alpha=.3)

ax.legend(loc='upper left')

ax = fig.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
# ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
# ax.spines['left'].set_position(('data',0))

fig.tight_layout()

canvas = FigureCanvas(fig)
sw.add_with_viewport(canvas)

toolbar = NavigationToolbar(canvas, myfirstwindow)
sw2.add_with_viewport(toolbar)

myfirstwindow.show_all()
Gtk.main()
