#!/usr/bin/env python
import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk

class Main(object):
    def __init__(self):
        self.win = gtk.Window()
        self.win.set_title("Volume Control Example")
        self.win.set_default_size(200, -1)
        self.win.connect("delete_event", lambda w,e: gtk.main_quit())
        hbox = gtk.HBox(False, 0)

        self.load_file = gtk.FileChooserButton("Choose Audio File")
        self.load_file.connect("selection-changed", self.on_file_selected)
        volume_button = gtk.VolumeButton()
        volume_button.connect("value-changed", self.on_volume_changed)

        hbox.pack_start(self.load_file, True, True, 0)
        hbox.pack_start(volume_button, False, True, 0)
  
        self.win.add(hbox)       
        self.win.show_all()

        self.player = gst.element_factory_make("playbin", "MultimediaPlayer")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)

    def on_file_selected(self, widget):
        self.player.set_property("uri", "file://" + self.load_file.get_filename())
        self.player.set_state(gst.STATE_PLAYING)

    def on_volume_changed(self, widget, value=0.5):
        print value
        self.player.set_property("volume", float(value))
        return True

    def on_message(self, bus, message):
        if message.type == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
        elif message.type == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            (err, debug) = message.parse_error()
            print "Error: %s" % err, debug           
    
if __name__ == "__main__":
    Main()
    gtk.main()


