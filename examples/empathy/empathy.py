#!/usr/bin/env python
import pygtk
pygtk.require("2.0")
import gtk
import empathygtk


account_setup_win = gtk.Window()

win = gtk.Window()
win.connect("destroy", lambda wid: gtk.main_quit())

vbox = gtk.VBox()
hbox = gtk.HBox()


account_chooser = empathygtk.AccountChooser()
vbox.pack_start(account_chooser)

# Filechooser to set your avatar
avatar_chooser = empathygtk.AvatarChooser()
vbox.pack_start(avatar_chooser)

chat_view = empathygtk.ChatView()
vbox.pack_start(chat_view)

# Account dialog takes a gtk.Window as an argument to show itself.
empathygtk.empathy_accounts_dialog_show(account_setup_win)


win.add(vbox)
win.show_all()

gtk.main()
