#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk

label = gtk.Label("Hello")

def print_callback(widget=None, text_box=None):
	label.set_text(text_box.get_text())

def clear_callback(widget=None, text_box=None):
	text_box.set_text("")
	label.set_text("")

def main():
	win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	win.connect("delete_event", lambda wid, we: gtk.main_quit())
	vbox = gtk.VBox(True, 2)
	win.add(vbox)

	text_box = gtk.Entry()  

	print_button = gtk.Button("Print Text")
	print_button.connect("clicked", print_callback, text_box)

	clear_button = gtk.Button("Clear Text")
	clear_button.connect("clicked", clear_callback, text_box)

	vbox.pack_start(label, True, True, 2)
	vbox.pack_start(text_box, True, True, 2)
	vbox.pack_start(print_button, True, True, 2)
	vbox.pack_start(clear_button, True, True, 2)

	win.show_all()
	   
if __name__ == "__main__":
	main()
	gtk.main()
