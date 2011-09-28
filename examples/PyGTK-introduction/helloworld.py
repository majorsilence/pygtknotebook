import pygtk
pygtk.require("2.0")
import gtk

label = gtk.Label("Hello World!")
win = gtk.Window()
win.add(label)
win.show_all()
gtk.main() 