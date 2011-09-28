#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk

class StatusbarTest(object):
	def __init__(self):
		win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		win.connect("delete_event", lambda wid, we: gtk.main_quit())
		vbox = gtk.VBox(False, 2)
		win.add(vbox)
		
		self.statusbar = gtk.Statusbar()
		self.context_id = self.statusbar.get_context_id("Status Test")
		
		self.text_entry = gtk.Entry()
		
		button = gtk.Button("Click Me")
		button.connect("clicked", self.button_callback)
		
		vbox.pack_start(self.text_entry, False, True, 2)
		vbox.pack_start(button, True, True, 2)
		vbox.pack_start(self.statusbar, False, True, 2)
		win.show_all()
	
	def button_callback(self, widget=None):
		self.statusbar.pop(self.context_id)
		self.statusbar.push(self.context_id, self.text_entry.get_text())

	
if __name__ == "__main__":
	StatusbarTest()
	gtk.main()
