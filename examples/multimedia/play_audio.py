#!/usr/bin/python
import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk

class Main(object):
    def __init__(self):
        self.multimedia_file=None
        self.init_gui()

        # Setup GStreamer
        self.player = gst.element_factory_make("playbin", "MultimediaPlayer")
        
        # The following 2 lines make sure only the audio from a video file is played.
        video_sink = gst.element_factory_make("fakesink", "fake for video")
        self.player.set_property("video-sink", video_sink)    
        
        bus = self.player.get_bus()
        bus.add_signal_watch()  
        #used to get messages that gstreamer emits
        bus.connect("message", self.on_message)

    def on_message(self, bus, message):
        if message.type == gst.MESSAGE_EOS: # End of Stream
            self.player.set_state(gst.STATE_NULL)
        elif message.type == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            (err, debug) = message.parse_error()
            print "Error: %s" % err, debug
    
    def init_gui(self):
        # Create the GUI
        self.win = gtk.Window()
        self.win.set_title("Play Audio Example")
        self.win.connect("delete_event", lambda w,e: gtk.main_quit())

        vbox = gtk.VBox(False, 0)
        hbox = gtk.HBox(False, 0)

        self.load_file = gtk.FileChooserButton("Choose Audio File")
        self.play_button = gtk.Button("Play", gtk.STOCK_MEDIA_PLAY)
        self.pause_button = gtk.Button("Pause", gtk.STOCK_MEDIA_PAUSE)
        self.stop_button = gtk.Button("Stop", gtk.STOCK_MEDIA_STOP)

        self.load_file.connect("selection-changed", self.on_file_selected)
        self.play_button.connect("clicked", self.on_play_clicked)
        self.pause_button.connect("clicked", self.on_pause_clicked)
        self.stop_button.connect("clicked", self.on_stop_clicked)

        hbox.pack_start(self.play_button, True, True, 0)
        hbox.pack_start(self.pause_button, True, True, 0)
        hbox.pack_start(self.stop_button, True, True, 0)

        vbox.pack_start(self.load_file, True, True, 0)
        vbox.add(hbox)
        self.win.add(vbox)
        
        self.win.show_all()

    def on_file_selected(self, widget):
        print "Selected: ", self.load_file.get_filename()
        self.multimedia_file = self.load_file.get_filename()

    def on_play_clicked(self, widget):
        print "play"
        self.player.set_property('uri', "file://" + self.multimedia_file)
        self.player.set_state(gst.STATE_PLAYING)

    def on_pause_clicked(self, widget):
        print "pause"
        self.player.set_state(gst.STATE_PAUSED)

    def on_stop_clicked(self, widget):
        print "stop"
        self.player.set_state(gst.STATE_NULL)

if __name__ == "__main__":
    Main()
    gtk.main()


