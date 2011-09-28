#!/usr/bin/env python
import os
import gobject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gtk

output_label = None
    
class DBusObject(dbus.service.Object):
    @dbus.service.signal('com.majorsilence.MessageInterface')
    def message_signal(self):
        return

    # Display and message to gtk label and return message to caller
    @dbus.service.method('com.majorsilence.MessageInterface', in_signature='', out_signature='s')
    def display_welcome_message(self):
        global output_label
        output_label.set_text("Welcome to dbus.")
        return "Welcome to dbus."

    # Set gtk label to the message that is passed
    @dbus.service.method(dbus_interface='com.majorsilence.MessageInterface', in_signature='s', out_signature='')
    def set_message(self, s):
        global output_label
        if not isinstance(s, dbus.String):
            print "not string"
            return
        output_label.set_text(s)
        
        #emit signal
        self.message_signal()

def main():
    # Create GTK Gui
    global output_label
    win = gtk.Window()
    win.connect("delete_event", lambda w,e:gtk.main_quit())
    output_label = gtk.Label("This message will change through using dbus.")
    win.add(output_label)
    win.show_all()
    
    # Start DBus Service
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.majorsilence.MessageService", session_bus)
    object = DBusObject(session_bus, "/TestObject")

    gtk.main()
    

if __name__ == "__main__":
    main()
    
