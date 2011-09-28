#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk


def button_callback(widget=None, data=None):
    print "%s was clicked." % data

def main():
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.connect("delete_event", lambda wid, we: gtk.main_quit())
    vbox = gtk.VBox(True, 2)
    win.add(vbox)
    
    button = gtk.Button("Click Me")
    button.connect("clicked", button_callback, "Button Click Me")
    vbox.pack_start(button, True, True, 2)
    
    win.show_all()
       
if __name__ == "__main__":
    main()
    gtk.main()
