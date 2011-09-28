import gobject, dbus 
from dbus.mainloop.glib import DBusGMainLoop

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
proxy_object = bus.get_object('org.gnome.Rhythmbox','/org/gnome/Rhythmbox/Player')
player = dbus.Interface(proxy_object, 'org.gnome.Rhythmbox.Player') 
print player.Introspect(dbus_interface='org.freedesktop.DBus.Introspectable')
