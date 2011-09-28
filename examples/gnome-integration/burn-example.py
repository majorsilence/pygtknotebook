import sys
# load module beneath
sys.path.append ('..')
import gtk, gobject
import nautilusburn


class BurnExample(object):
    def __init__(self):
        self.selected_drive={"name":"None", "device":"None"}
        self.drive=None
        win = gtk.Window()
        win.connect("delete_event", lambda w,e: gtk.main_quit())
        
        vbox = gtk.VBox(False, 0)
        drives = self.init_recording_devices()
        drives.connect('changed', self.on_drives_changed)
        
        erase_disc_button = gtk.Button("Erase Disc")
        erase_disc_button.connect("clicked", self.erase_disc)
        
        vbox.pack_start(drives, False, False, 0)
        vbox.pack_start(erase_disc_button, False, False, 0)
        
        win.add(vbox)
        win.show_all()
        
    def init_recording_devices(self):
        drives = nautilusburn.DriveSelection()
        drives.set_property('show-recorders-only', True)
        drives.show()
        
        #Remove the next line
        #drives.append_text("number two")
        
        self.selected_drive["name"] = drives.get_active_text()
        self.selected_drive["device"] = drives.get_device()
        self.drive = drives.get_drive()
        #print drives.get_active()
        #print drives.get_default_device()
        #print drives.get_device()
        #print drives.get_drive()
        #drives.set_active()
        #drives.set_device()
        return drives
        
    def erase_disc(self, widget):
        drvmon = nautilusburn.DriveMonitor()
        #for drive in drvmon.get_recorder_drives(): 
        #    print drive.get_name_for_display(), drive, drive.get_device()
        drive = drvmon.get_recorder_drives()[0]
        print drive.get_name_for_display()
        print drive
        print drive.get_device()

        
        r = nautilusburn.Recorder()
        r.connect('progress-changed', self.on_blank_progress_changed)
        r.blank_disc (drive, nautilusburn.RECORDER_BLANK_FAST, True)
        print "done"
    
    # Callbacks
    def on_drives_changed(self, widget=None):
        self.selected_drive["name"] = widget.get_active_text()
        self.selected_drive["device"] = widget.get_device()
        self.drive = widget.get_drive()
        print widget.get_active_text()
        print widget.get_device()
        
    def on_blank_progress_changed(self, widget, fraction, somethingelse):
        print dir(widget)
        print dir(somethingelse)
        if fraction > 0:
            print "fraction: ", fraction
            print "Percent: ", fraction*100
        
if __name__ == "__main__":
    app = BurnExample()
    gtk.main()
    
