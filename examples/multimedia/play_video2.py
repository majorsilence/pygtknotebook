#!/usr/bin/python
import os
import sys
import time

import pygtk
pygtk.require('2.0')
import gtk
import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')
import gst

# import discoverer so we can get info about our video file
from gst.extend import discoverer


class MediaInfo:
    """
    Create a nice simple wrapper around the gstreamer file info
    FileInfo code is borrowd from the gst-discover example taht comes
    with the pygst source release.
    
    It appears to be licensed under the 
    GNU LESSER GENERAL PUBLIC LICENSE Version 2.1
    Just like the rest of the code in the books.
    """
    
    def __init__(self, path):
        def discovered(d, is_media):
            if is_media:
                self.succeed(d)
            else:
                self.fail(path)    
        self.__finished = False
        self.__is_media=False
        self.__video_width = 0
        self.__video_height = 0
        self.__is_video = False
        self.__is_audio = False
    
        # other video info
        self.__mimetype = ""
        self.__video_caps = ""
        self.__video_length = 0
        self.__frame_rate = ""
        
        # audio info
        self.__audio_caps = ""
        self.__audio_format = ""
        self.__sample_audio_rate = 0
        self.__sample_audio_width = 0
        self.__sample_audio_depth = 0
        self.__audio_length = 0
        self.__audio_channels = 0
        
        self.__is_fullscreen = False
        print "path: ", path

        d = discoverer.Discoverer(path)
        #print help(d.discover)
        d.connect('discovered', discovered)
        d.discover()
    
    def fail(self, path):
            print "error: %r does not appear to be a media file" % path
            self.__is_media = False

    def succeed(self, d):
        print "File discover success"
        self.__is_media = True
        self.__mimetype = d.mimetype
        self.__is_video = d.is_video
        if self.__is_video:
            self.__video_caps = d.videocaps
            self.__video_width = d.videowidth
            self.__video_height = d.videoheight 
            # Retrieve the video length in minute
            self.__video_length = ((d.videolength / gst.MSECOND) / 1000) / 60
            self.__frame_rate = '%s/%s' % (d.videorate.num, d.videorate.denom)


        self.__is_audio = d.is_audio
        if self.__is_audio:
            self.__audio_caps = d.audiocaps
            self.__audio_format = d.audiofloat
            self.__sample_audio_rate = d.audiorate
            self.__sample_audio_width = d.audiowidth
            self.__sample_audio_depth = d.audiodepth
            # Retrieve the audio length in minute
            self.__audio_length = ((d.audiolength / gst.MSECOND) / 1000) / 60
            self.__audio_channels = d.audiochannels
            
        self.__finished = True
    
    def poll(self):
        return self.__finished
    
    def is_media(self):
        return self.__is_media
    
    def is_video(self):
        return self.__is_video
        
    def is_audio(self):
        return self.__is_audio
    
    def get_width(self):
        return self.__video_width
    
    def get_height(self):
        return self.__video_height


class GstPlayer(object):
    """
    GstPlayer is a class to control gstreamer.  It plays video and audio
    and receives messages from the gestreamer bus.
    It uses a videowidget that is passed in from the gui. 
    """
    def __init__(self, videowidget):
        # Setup GStreamer  
        self.videowidget = videowidget
        self.player = gst.element_factory_make("playbin", "MultimediaPlayer")

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        #used to get messages that gstreamer emits
        bus.connect("message", self.on_message)
        #used for connecting video to your application
        bus.connect("sync-message::element", self.on_sync_message)        

    def set_location(self, location):
        self.player.set_property('uri', "file://" + location)
    
    def play(self):
        print "playing"
        self.player.set_state(gst.STATE_PLAYING)

    def pause(self):
        print "paused"
        self.player.set_state(gst.STATE_PAUSED)

    def stop(self):
        print "stoped"
        self.player.set_state(gst.STATE_NULL)

    def on_message(self, bus, message):
        if message.type == gst.MESSAGE_EOS: # End of Stream
            self.player.set_state(gst.STATE_NULL)
        elif message.type == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            (err, debug) = message.parse_error()
            print "Error: %s" % err, debug
            
    def on_sync_message(self, bus, message):
        if message.structure is None:
            return False
        if message.structure.get_name() == "prepare-xwindow-id":
            self.videowidget.set_sink(message.src)
            message.src.set_property('force-aspect-ratio', True)

class VideoWidget(gtk.DrawingArea):
    """
    Extend gtk.DrawingArea to create our own video widget.
    """
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.imagesink = None
        self.unset_flags(gtk.DOUBLE_BUFFERED)

    def do_expose_event(self, event):
        if self.imagesink:
            self.imagesink.expose()
            return False
        else:
            return True

    def set_sink(self, sink):
        if sys.platform=="win32":
            win_id = self.window.handle
        else:
            win_id = self.window.xid
        assert win_id
        self.imagesink = sink
        self.imagesink.set_xwindow_id(win_id)
 

class Main(object):
    """
    The Main class is the Gui.  It creates an instance of the GstPlayer class
    and the FileInfo class.
    It is what the user interacts with and controls what happens.
    """
    def __init__(self):
        #Store the location of the multimedia file
        self.multimedia_file = None
        
        # To be used with the FileInfo Class
        self.file_info = None

        # Create the GUI
        self.win = gtk.Window()
        self.win.set_title("Play Video Example 2")
        self.win.connect("delete_event", lambda w,e: gtk.main_quit())

        vbox = gtk.VBox(False, 0)
        self.control_box = gtk.HBox(False, 0)

        # Control Buttons
        self.load_file_button = gtk.FileChooserButton("Choose Audio File")
        self.play_button = gtk.Button("Play", gtk.STOCK_MEDIA_PLAY)
        self.pause_button = gtk.Button("Pause", gtk.STOCK_MEDIA_PAUSE)
        self.stop_button = gtk.Button("Stop", gtk.STOCK_MEDIA_STOP)

        # Video Widget Stuff
        self.videowidget = VideoWidget()
        self.videowidget.set_size_request(400, 250)

        # Signals and Callbacks
        self.load_file_button.connect("selection-changed", self.on_file_selected)
        self.play_button.connect("clicked", self.on_play_clicked)
        self.pause_button.connect("clicked", self.on_pause_clicked)
        self.stop_button.connect("clicked", self.on_stop_clicked)
        
        # Fullscreen stuff
        self.win.connect("key-press-event", self.on_win_key_press_event)
        self.win.connect("window-state-event", self.on_window_state_event)

        self.control_box.pack_start(self.play_button, False, True, 0)
        self.control_box.pack_start(self.pause_button, False, True, 0)
        self.control_box.pack_start(self.stop_button, False, True, 0)
        
        vbox.pack_start(self.load_file_button, False, True, 0)
        vbox.pack_start(self.videowidget, True, True, 0) # You want to expand the video widget or else you cannot see it
        vbox.pack_start(self.control_box, False, True, 0)
        self.win.add(vbox)
        
        self.win.show_all()

        self.gst_player = GstPlayer(self.videowidget)


    def fullscreen_mode(self):
        """
        Called from the on_win_key_press_event method.
        If the program is in fullscreen this method will unfullscreen it.
        If the program is not in fullscreen it will set it to fullscreen.
        This method will also hide the controls while in fullscreen mode.
        """
        if self.__is_fullscreen:
            self.win.unfullscreen()
            self.control_box.show()
            self.load_file_button.show()
        else:
            self.control_box.hide()
            self.load_file_button.hide()
            self.win.fullscreen()
    
    def on_win_key_press_event(self, widget, event):
        """
        Handle any key press event on the main window.
        This method is being used to detect when the ESC key
        is being pressed in fullscreen to take the 
        window out of fullscreen
        """
        key = gtk.gdk.keyval_name(event.keyval)
        if key == "Escape" or key == "f":
            self.fullscreen_mode()  
    
    def on_window_state_event(self, widget, event):
        """
        Detect window state events to determine whether in fullscreen
        or not in fullscreen
        """

        self.__is_fullscreen = bool(event.new_window_state &
                                            gtk.gdk.WINDOW_STATE_FULLSCREEN)
        print "Is fullscreen: ", self.__is_fullscreen

    def on_file_selected(self, widget):
        print "Selected: ", self.load_file_button.get_filename()
        self.multimedia_file = self.load_file_button.get_filename()
        
        # Do not call method from here immedialty.  
        # FileInfo.poll() will return false when it is ready.  Usually a second or two.
        self.file_info = MediaInfo(self.multimedia_file)
        
        self.gst_player.set_location(self.multimedia_file)    

    def on_play_clicked(self, widget):
        print "play clicked"
        print "Video (width, height): ", self.file_info.get_width(), self.file_info.get_height()
        self.videowidget.set_size_request(self.file_info.get_width(), self.file_info.get_height())
        self.gst_player.play()

    def on_pause_clicked(self, widget):
        print "pause clicked"
        self.gst_player.pause()

    def on_stop_clicked(self, widget):
        print "stop clicked"
        self.gst_player.stop()


    
if __name__ == "__main__":
    Main()
    gtk.main()


