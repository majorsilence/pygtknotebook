#!/usr/bin/python

import sys
import time
import gobject

import pygst
pygst.require("0.10")
import gst

import pygtk
import gtk


class Main(object):
    def __init__(self):
        self.multimedia_file=""
        # Used with gstreamer seeking
        self.time_format = gst.Format(gst.FORMAT_TIME)
        self.duration = None
        self.is_playing = False
        
        # Create the GUI
        self.win = gtk.Window()
        self.win.set_title("Play Video Example")
        self.win.connect("delete_event", lambda w,e: gtk.main_quit())
        
        vbox = gtk.VBox(False, 0)
        hbox = gtk.HBox(False, 0)
        
        self.load_file = gtk.FileChooserButton("Choose Audio File")
        self.play_button = gtk.Button("Play", gtk.STOCK_MEDIA_PLAY)
        self.pause_button = gtk.Button("Pause", gtk.STOCK_MEDIA_PAUSE)
        self.stop_button = gtk.Button("Stop", gtk.STOCK_MEDIA_STOP)
        
        # Create a scale with an adjustment of one
        #gtk.Adjustment(value=0, lower=0, upper=0, step_incr=0, page_incr=0, page_size=0)
        self.adjustment = gtk.Adjustment(0.0, 0.00, 100.0, 0.1, 1.0, 1.0)
        self.seeker = gtk.HScale(self.adjustment)
        self.seeker.set_draw_value(False) # Do not draw the position percent or emit the format-value signal
        self.seeker.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
        self.time_label = gtk.Label("00:00 / 00:00")
        
        self.videowidget = gtk.DrawingArea()
        self.videowidget.set_size_request(400, 250)
        
        # Signals
        self.load_file.connect("selection-changed", self.on_file_selected)
        self.play_button.connect("clicked", self.on_play_clicked)
        self.pause_button.connect("clicked", self.on_pause_clicked)
        self.stop_button.connect("clicked", self.on_stop_clicked)
           
        self.seeker.connect("button-release-event", self.seeker_button_release_event)
        
        
        # Pack the Widgets
        hbox.pack_start(self.play_button, False, True, 0)
        hbox.pack_start(self.pause_button, False, True, 0)
        hbox.pack_start(self.stop_button, False, True, 0)
        hbox.pack_start(self.seeker, True, True, 0)
        hbox.pack_start(self.time_label, False, False, 0)
        
        vbox.pack_start(self.load_file, False, True, 0)
        vbox.pack_start(self.videowidget, True, True, 0) # You want to expand the video widget or else you cannot see it
        vbox.pack_start(hbox, False, True, 0)
        self.win.add(vbox)
        
        self.win.show_all()
        
        # Setup GStreamer
        self.player = gst.element_factory_make("playbin", "MultimediaPlayer")
        
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        
        #used to get messages that gstreamer emits
        bus.connect("message", self.on_message)
        
        #used for connecting video to your application
        bus.connect("sync-message::element", self.on_sync_message)
        
    def on_file_selected(self, widget):
        # When file load reset duration to none for use in the update_time_label method
        self.duration = None
        
        print "Selected: ", self.load_file.get_filename()
        self.multimedia_file = self.load_file.get_filename()
        #self.player.set_property('uri', "file://" + self.multimedia_file)

    def on_play_clicked(self, widget):
        print "play"
        self.player.set_property('uri', "file://" + self.multimedia_file)
        self.player.set_state(gst.STATE_PLAYING)
        self.is_playing = True
        # Once a second update the self.time_label to display the correct location
        # Stop calling on return value of False
        timer=gobject.timeout_add(1000, self.update_time_label)

    def on_pause_clicked(self, widget):
        print "pause"
        self.player.set_state(gst.STATE_PAUSED)
        self.is_playing = False

    def on_stop_clicked(self, widget):
        print "stop"
        self.player.set_state(gst.STATE_NULL)
        self.is_playing = False

    def on_message(self, bus, message):
        if message.type == gst.MESSAGE_EOS: # End of Stream
            self.player.set_state(gst.STATE_NULL)
            self.is_playing = False
        elif message.type == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            (err, debug) = message.parse_error()
            print "Error: %s" % err, debug
            
    def on_sync_message(self, bus, message):
        if message.structure is None:
            return False
        if message.structure.get_name() == "prepare-xwindow-id":
            #assert self.videowidget.window.xid
            if sys.platform=="win32":
                win_id = self.videowidget.window.handle
            else:
                win_id = self.videowidget.window.xid
                
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(win_id)
    
    # Seeking and Position Methods
    
    # Position methods
    def update_time_label(self):
        """
        Update the time_label to display the current location in the media file
        """
        if self.is_playing == False:
            print "return false"
            return False
        print "update_time_label"
        
        if self.duration == None:
            try:
                self.length = self.player.query_duration(self.time_format, None)[0]
                self.duration = self.convert_time(self.length)
            except:
                self.duration = None

        if self.duration != None:
            self.current_position = self.player.query_position(self.time_format, None)[0]
            current_position_formated = self.convert_time(self.current_position)
            self.time_label.set_text(current_position_formated + "/" + self.duration )
            
            # Update the seek bar
            #gtk.Adjustment(value=0, lower=0, upper=0, step_incr=0, page_incr=0, page_size=0)
            percent = (float(self.current_position)/float(self.length))*100.0
            adjustment = gtk.Adjustment(percent, 0.00, 100.0, 0.1, 1.0, 1.0)
            self.seeker.set_adjustment(adjustment)
            
        print "return true"
        return True
        
    def convert_time(self, time=None):
        # convert_ns function from:
        # http://pygstdocs.berlios.de/pygst-tutorial/seeking.html
        # LGPL Version 3  - Copyright: Jens Persson
        if time==None:
            return None
        hours = 0
        minutes = 0
        seconds = 0
        time_string = ""
        
        time = time / 1000000000
        # gst.NSECOND
        
        if time >= 3600:
            hours = time / 3600
            time = time - (hours * 3600)
        if time >= 60:
            minutes = time / 60
            time = time - (minutes * 60)
        #remaining time is seconds
        seconds = time
        # return time in Hours:Minutes:seconds format
        time_string = time_string + str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        print time_string
        return time_string
       
    # Seeking Methods 
    def seeker_button_release_event(self, widget, event):
        print "seeker_button_release_event"
        value =  widget.get_value()
        
        if self.is_playing == True:
            duration = self.player.query_duration(self.time_format, None)[0]
            time = value * (duration / 100)
            print self.convert_time(time)
            self.player.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH, time)
            
            #pos_int = self.player.query_position(self.time_format, None)[0]
            #seek_ns = pos_int + (10 * 1000000000)
            #self.player.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH, seek_ns)


if __name__ == "__main__":
    Main()
    gtk.main()


