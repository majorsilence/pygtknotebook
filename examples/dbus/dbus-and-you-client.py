#!/usr/bin/env python
import os
import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gtk

class DBusClient(object):
    def __init__(self):
        # Do before session or system bus is created.
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        
        self.bus = dbus.SessionBus()
        
        self.proxy = self.bus.get_object('com.majorsilence.MessageService', '/TestObject')
        self.control_interface = dbus.Interface(self.proxy, 'com.majorsilence.MessageInterface')
        print self.control_interface.Introspect(dbus_interface='org.freedesktop.DBus.Introspectable')
        

        self.bus.add_signal_receiver(self.on_message_recieved, dbus_interface="com.majorsilence.MessageInterface", signal_name="message_signal")
        
        win = gtk.Window()
        win.connect("delete_event", lambda w,e:gtk.main_quit())
        vbox = gtk.VBox()
        hbox = gtk.HBox()

        self.text_message=gtk.Entry()

        set_message=gtk.Button("Set Message")
        display_message=gtk.Button("Display Welcome Message")

        set_message.connect("clicked", self.on_set_message_clicked)
        display_message.connect("clicked", self.on_display_message_clicked)
        
        hbox.pack_start(set_message, False, True, 0)
        hbox.pack_start(display_message, False, True, 0)
        vbox.pack_start(self.text_message, False, True, 0)
        vbox.pack_start(hbox, False, True, 0)
        
        win.add(vbox)
        win.show_all()
    
    def on_message_recieved(self):
        print "message_signal caught"
        
    def on_set_message_clicked(self, widget):
        message = self.text_message.get_text()
        self.control_interface.set_message(message)
    
    def on_display_message_clicked(self, widget):
        print self.control_interface.display_welcome_message()

if __name__ == "__main__":
    app = DBusClient()
    gtk.main()
