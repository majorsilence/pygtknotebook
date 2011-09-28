#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk


def save_callback(widget=None):
	print "Save menu item was pressed"

def quit_callback(widget=None):
	print "Quit menu item was pressed"
	gtk.main_quit()

def about_callback(widget=None):
	print "About menu item was pressed"

def main():
	win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	win.connect("delete_event", lambda wid, we: gtk.main_quit())
	win.set_size_request(400, 30)
	vbox = gtk.VBox(True, 2)
	win.add(vbox)

	menubar = gtk.MenuBar()
	
	# Create main file menus
	file_item = gtk.MenuItem("_File")
	help_item = gtk.MenuItem("_Help")

	file_item_sub = gtk.Menu() # container to hold menuitems
	save = gtk.MenuItem("_Save")
	quit = gtk.MenuItem("_Quit")
	file_item_sub.append(save)
	file_item_sub.append(quit)
	
	help_item_sub = gtk.Menu()
	about = gtk.MenuItem("_About")
	help_item_sub.append(about)
	
	#Main File menu appending
	file_item.set_submenu(file_item_sub)
	help_item.set_submenu(help_item_sub)
	menubar.append(file_item)
	menubar.append(help_item)

	save.connect("activate", save_callback)
	quit.connect("activate", quit_callback)
	about.connect("activate", about_callback)

	vbox.pack_start(menubar, True, True, 2)

	win.show_all()
	
if __name__ == "__main__":
	main()
	gtk.main()
