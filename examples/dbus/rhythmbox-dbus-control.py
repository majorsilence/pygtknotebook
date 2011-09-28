#!/usr/bin/env python
import os
import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gtk

class DBusExample(object):
    def __init__(self):
        # Do before session or system bus is created.
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        
        self.bus = dbus.SessionBus()
        # service/bus name: org.gnome.Rhythmbox
        # Objects path: /org/gnome/Rhythmbox/Player
        #          /org/gnome/Rhythmbox/Shell
        #          /org/gnome/Rhythmbox/PlaylistManager
        # Interface: org.gnome.Rhythmbox.Player
        # Used to allow accessing specific exposed methods

        self.proxy_object = self.bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player')
        self.player = dbus.Interface(self.proxy_object, 'org.gnome.Rhythmbox.Player')
        
        
        self.bus.add_signal_receiver(self.on_song_changed, dbus_interface="org.gnome.Rhythmbox.Player", signal_name="playingUriChanged")
        
        self.init_gui()
        #self.list_available_commands()

    def list_available_commands(self):
        """
        List all commands available.  Prints the xml.
        """
        print self.player.Introspect(dbus_interface='org.freedesktop.DBus.Introspectable')
        
    # gtk gui stuff
    def init_gui(self):
        win = gtk.Window()
        win.connect("delete_event", lambda w,e:gtk.main_quit())
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        
        self.output = gtk.Label("")
        vbox.pack_start(self.output, False, True, 0)
        
        mute=gtk.Button("Mute")
        play_pause=gtk.Button("Play/Pause")
        previous=gtk.Button("Previous")
        next=gtk.Button("Next")
        
        mute.connect("clicked", self.on_mute_clicked)
        play_pause.connect("clicked", self.on_play_pause_clicked)
        previous.connect("clicked", self.on_previous_clicked)
        next.connect("clicked", self.on_next_clicked)
        
        hbox.pack_start(mute, False, True, 0)
        hbox.pack_start(play_pause, False, True, 0)
        hbox.pack_start(previous, False, True, 0)
        hbox.pack_start(next, False, True, 0)  
        
        vbox.pack_start(hbox, False, True, 0) 
        win.add(vbox)
        win.show_all()
        
    def on_mute_clicked(self, widget):
        """
        Mute the volume of Rythmbox.
        If volume is muted, unmute.
        If volue is not muted, mute.
        """
        if self.player.getMute():
            self.player.setMute(False)
        else:
            self.player.setMute(True)
        
    def on_play_pause_clicked(self, widget):
        """
        If currently pause, play.
        If currently playing, pause
        """
        if self.player.getPlaying():
            self.player.playPause(False)
        else:
            self.player.playPause(True)
        #self.player.playPause("Play or Pause")
    
    def on_previous_clicked(self, widget):
        """
        Play the previous song
        """
        self.player.previous()
        
    def on_next_clicked(self, widget):
        """
        Play the next song.
        """
        self.player.next()   
    
    def on_song_changed(self, data):
        """
        On song change, retrieve the current playing tracks uri, 
        separte into a path and filename and display in a label 
        in the gui.
        """
        path, filename = os.path.split(self.player.getPlayingUri())
        # could also use data instead of getPlayingUri()
        self.output.set_text("Path: " + path + "\nFilename: " + filename)

if __name__ == "__main__":
    app = DBusExample()
    gtk.main()
