#!/usr/bin/python
import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk

class InstallMissingCodecExample(object):
    def __init__(self):
        # Gtk Gui
        self.win = gtk.Window()
        self.win.set_title("Install Missing Codec Example")
        self.win.connect("delete_event", lambda w,e: gtk.main_quit())
        self.load_file = gtk.FileChooserButton("Choose Audio File")
        self.load_file.connect("selection-changed", self.on_file_selected)
        self.win.add(self.load_file)
        self.win.show_all()

        # Setup GStreamer
        self.player = gst.element_factory_make("playbin", "MultimediaPlayer")
        
        bus = self.player.get_bus()
        bus.add_signal_watch()  
        bus.connect("message", self.on_message)
        
    def on_file_selected(self, widget):
        print "Selected: ", self.load_file.get_filename()
        multimedia_file = self.load_file.get_filename()
        self.player.set_property('uri', "file://" + multimedia_file)
        self.play()
     
    def play(self):
        self.player.set_state(gst.STATE_PLAYING)

    # Codec Buddy Methods
    def on_message(self, bus, message):
        import gst
        if message.type == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            (err, debug) = message.parse_error()
            print "Error: %s" % err, debug       
        elif message.type == gst.MESSAGE_EOS: # End of Stream
            self.player.set_state(gst.STATE_NULL)
        elif message.type == gst.MESSAGE_ELEMENT:
            """
            CodicBuddy Stuff
            """
            st = message.structure
            if st and st.get_name().startswith('missing-'):
                self.player.set_state(gst.STATE_NULL)
                if gst.pygst_version >= (0, 10, 10):
                    import gst.pbutils
                    detail = gst.pbutils.missing_plugin_message_get_installer_detail(message)
                    context = gst.pbutils.InstallPluginsContext()
                    gst.pbutils.install_plugins_async([detail], context, self.install_plugin)
                    
    def install_plugin(self, result):
        if result == gst.pbutils.INSTALL_PLUGINS_SUCCESS:
            gst.update_registry()
            self.play()
            return
        if result == gst.pbutils.INSTALL_PLUGINS_USER_ABORT:
            dialog = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL, 
                type=gtk.MESSAGE_INFO, 
                buttons=gtk.BUTTONS_OK, 
                message_format="Plugin installation aborted.")
            dialog.run()
            dialog.hide()
            return

        error.show("Error", "failed to install plugins: %s" % str(result))

if __name__ == "__main__":
    InstallMissingCodecExample()
    gtk.main()
