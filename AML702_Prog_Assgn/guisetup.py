#!/usr/bin/python3

from gi.repository import Gtk

from matplotlib.figure import Figure
from numpy import sin, cos, pi, linspace, log
import numpy as np
#Possibly this rendering backend is broken currently
#from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

from app import numintegrals as nigl

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

class MethodDetailsBox(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        self. set_selection_mode(Gtk.SelectionMode.NONE)

        mnames = {'none':'None',
                  'trapz':'Trapezoidal',
                  'simp13':'Simpson\'s 1/3',
                  'simp38':'Simpson\'s 3/8',
                  'glquad':'Gauss-Legendre Quadrature'}

        self.zerofn = self.fexact = self.fapprox = lambda x: np.zeros(np.shape(x))
        self.a = 0; self.b = 1

        # Adding the ComboBox with the name
        self.mname_combo = Gtk.ComboBoxText.new();
        self.mname_combo.append('none','None')
        self.mname_combo.append('trapz','Trapezoidal')
        self.mname_combo.append('simp13','Simpson\'s 1/3')
        self.mname_combo.append('simp38','Simpson\'s 3/8')
        self.mname_combo.append('glquad','Gauss-Legendre Quadrature')
        self.mname_row = Gtk.ListBoxRow()
        self.mname_row.add(self.mname_combo)
        self.add(self.mname_row)

        self.mname_combo.connect('changed',self.on_method_changed)

        # Packing up the "Number of Steps" row
        self.numsteps_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.numsteps_row = Gtk.ListBoxRow()
        self.numsteps_row.add(self.numsteps_box)
        label1 = Gtk.Label('Steps: ', xalign=0)
        self.numsteps_box.pack_start(label1,False,False,0)
        self.numsteps_sb = Gtk.SpinButton.new_with_range(1,100,1)
        self.numsteps_box.pack_end(self.numsteps_sb,False,False,0)
        self.add(self.numsteps_row)
        
        self.numsteps_sb.connect('value-changed',self.on_method_changed)

        # Packing up the "Order" row (Useful for GLQ)
        self.order_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.order_row = Gtk.ListBoxRow()
        self.order_row.add(self.order_box)
        label1 = Gtk.Label('Order: ', xalign=0)
        self.order_box.pack_start(label1,False,False,0)
        self.order_sb = Gtk.SpinButton.new_with_range(1,15,1)
        self.order_box.pack_end(self.order_sb,False,False,0)
        self.add(self.order_row)

        self.order_sb.connect('value-changed',self.on_method_changed)
       
        # Packing up the "Step Size" row
        self.stepsize_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.stepsize_row = Gtk.ListBoxRow()
        self.stepsize_row.add(self.stepsize_box)
        label1 = Gtk.Label('Step Size: ', xalign=0)
        self.stepsize_box.pack_start(label1,False,False,0)
        self.stepsize_entry = Gtk.Entry()
        self.stepsize_entry.set_alignment(1.0)
        self.stepsize_box.pack_end(self.stepsize_entry,False,False,0)
        self.insert(self.stepsize_row,1)

        # Packing up the "Result" row
        self.result_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.result_row = Gtk.ListBoxRow()
        self.result_row.add(self.result_box)
        label1 = Gtk.Label('Result: ', xalign=0)
        self.result_box.pack_start(label1,False,False,0)
        self.result_label = Gtk.Label('', xalign=1.0)
        self.result_box.pack_end(self.result_label,False,False,0)
        self.add(self.result_row)

        self.result = 0        

        # The tree that shows the points where evaluation is done
        self.liststore = Gtk.ListStore(float, float, float)
        self.points_tree = Gtk.TreeView(model=self.liststore)
        self.points_scroll = Gtk.ScrolledWindow()
        self.points_scroll.add(self.points_tree)
        self.points_scroll.set_min_content_height(150)
        self.points_tree.set_vexpand(True)
        self.add(self.points_scroll)

        self.xrenderer = Gtk.CellRendererText()
        self.xcolumn = Gtk.TreeViewColumn("xi", self.xrenderer, text=0)
        self.xcolumn.set_expand(True)
        self.xcolumn.set_alignment(0.5)
        self.points_tree.append_column(self.xcolumn)

        self.yrenderer = Gtk.CellRendererText()
        self.ycolumn = Gtk.TreeViewColumn("f(xi)", self.yrenderer, text=1)
        self.ycolumn.set_expand(True)
        self.ycolumn.set_alignment(0.5)
        self.points_tree.append_column(self.ycolumn)
        
        self.wrenderer = Gtk.CellRendererText()
        self.wcolumn = Gtk.TreeViewColumn("wi", self.wrenderer, text=2)
        self.wcolumn.set_expand(True)
        self.wcolumn.set_alignment(0.5)
        self.points_tree.append_column(self.wcolumn)

        self.xis = self.fxis = self.wis = []
 
        self.mc = None
        self.last_methodid = ''

        # TODO: How to make it all work fine with the default set to "None"?
        self.mname_combo.set_active_id('none')

    def on_method_changed(self,widget):
        # TODO: Get the id of the selected method
        methodid = self.mname_combo.get_active_id()
        
        # TODO: Calculate approximate integral (Do it before all the view updates so that the answer is ready)

        self.refresh_data()

        if self.mc!=None:
            self.mc.plotexact()
            # print('Should have been replot')

        if self.last_methodid == methodid: return
        else: self.last_methodid = methodid
        
        # Change views as per ID
        # self.remove(self.order_row)
        # self.remove(self.stepsize_row)
        # self.remove(self.numsteps_row)
        self.order_row.set_visible(False)
        self.stepsize_row.set_visible(False)
        self.numsteps_row.set_visible(False)
        
        if methodid=='trapz':
            self.stepsize_row.set_visible(True)
            self.numsteps_row.set_visible(True)
            # self.insert(self.stepsize_row,1)
            # self.insert(self.numsteps_row,2)
        elif methodid=='simp13':
            self.stepsize_row.set_visible(True)
            self.numsteps_row.set_visible(True)
            # self.insert(self.stepsize_row,1)
            # self.insert(self.numsteps_row,2)
        elif methodid=='simp38':
            self.stepsize_row.set_visible(True)
            self.numsteps_row.set_visible(True)
            # self.insert(self.stepsize_row,1)
            # self.insert(self.numsteps_row,2)
        elif methodid=='glquad':
            # self.insert(self.order_row,1)
            self.order_row.set_visible(True)

    def refresh_data(self):
        methodid = self.mname_combo.get_active_id()
        
        if methodid=='none':
            self.result,self.xis,self.fxis,self.wis,self.fapprox \
                = '',[],[],[],self.zerofn
        if methodid=='trapz':
            self.result,self.xis,self.fxis,self.wis,self.fapprox \
                = nigl.intgl_trapz(self.fexact,self.a,self.b,self.numsteps_sb.get_value_as_int())
        elif methodid=='simp13':
            self.result,self.xis,self.fxis,self.wis,self.fapprox \
                = nigl.intgl_simp13(self.fexact,self.a,self.b,self.numsteps_sb.get_value_as_int())
        elif methodid=='simp38':
            self.result,self.xis,self.fxis,self.wis,self.fapprox \
                = nigl.intgl_simp38(self.fexact,self.a,self.b,self.numsteps_sb.get_value_as_int())
        elif methodid=='glquad':
            self.result,self.xis,self.fxis,self.wis,self.fapprox \
                = nigl.intgl_glquad(self.fexact,self.a,self.b,self.order_sb.get_value_as_int())

        # print(self.fapprox([1,0]))

        self.liststore.clear()
        for i in zip(self.xis,self.fxis,self.wis): self.liststore.append(i)

        self.result_label.set_text(str(self.result))
        
    def set_exact_function_and_bounds(self,fexact,a,b):
        self.fexact = fexact
        self.a = a
        self.b = b
        self.refresh_data()

if __name__ == '__main__':
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    md_box = MethodDetailsBox()
    window.add(md_box)
    window.show_all()
    Gtk.main()
