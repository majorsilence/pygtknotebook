#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk


def button_callback(widget=None):
	dialog = gtk.MessageDialog(parent = None,
		buttons = gtk.BUTTONS_YES_NO, flags = gtk.DIALOG_DESTROY_WITH_PARENT,
		type = gtk.MESSAGE_QUESTION, message_format = "Is this a good example?")
	dialog.set_title("MessageDialog Example")
	result = dialog.run()
	dialog.destroy()
	if result == gtk.RESPONSE_YES:
		print "Yes was clicked"
	elif result == gtk.RESPONSE_NO:
		print "No was clicked"

def main():
	win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	win.connect("delete_event", lambda wid, we: gtk.main_quit())
	vbox = gtk.VBox(True, 2)
	win.add(vbox)

	button = gtk.Button("Show Dialog")
	button.connect("clicked", button_callback)
	vbox.pack_start(button, True, True, 2)

	win.show_all()

if __name__ == "__main__":
	main()
	gtk.main()
