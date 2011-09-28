#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk

def button_callback(widget=None, spin=None):
    print spin.get_value()
    print spin.get_value_as_int()

def main():
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.connect("delete_event", lambda wid, we: gtk.main_quit())
    vbox = gtk.VBox(True, 2)
    win.add(vbox)
    
    #gtk.Adjustment(value=0, lower=0, upper=0, step_incr=0, page_incr=0, page_size=0) 
    adjustment = gtk.Adjustment(0, 0, 100, 1, 5, 0)
    spin = gtk.SpinButton(adjustment, 0, 0)
    vbox.pack_start(spin, True, True, 2)

    button = gtk.Button("Print Selected Item")
    button.connect("clicked", button_callback, spin)
    vbox.pack_start(button, True, True, 2)

    win.show_all()


if __name__ == "__main__":
    main()
    gtk.main()
