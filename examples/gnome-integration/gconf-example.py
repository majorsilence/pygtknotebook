#!/usr/bin/env python
#
# This program demonstrates how to use GConf.  The key thing is that
# the main window and the prefs dialog have NO KNOWLEDGE of one
# another as far as configuration values are concerned; they don't
# even have to be in the same process. That is, the GConfClient acts
# as the data "model" for configuration information; the main
# application is a "view" of the model; and the prefs dialog is a
# "controller."
#
# You can tell if your application has done this correctly by
# using "gconftool" instead of your preferences dialog to set
# preferences. For example:
# 
# gconftool --type=string --set /apps/basic-gconf-app/foo "My string"
# 
# If that doesn't work every bit as well as setting the value
# via the prefs dialog, then you aren't doing things right. ;-)
#
#
# If you really want to be mean to your app, make it survive
# this:
# 
# gconftool --break-key /apps/basic-gconf-app/foo
# 
# Remember, the GConf database is just like an external file or
# the network - it may have bogus values in it. GConf admin
# tools will let people put in whatever they can think of.
# 
# GConf does guarantee that string values will be valid UTF-8, for
# convenience.
# 

# Throughout, this program is letting GConfClient use its default
# error handlers rather than checking for errors or attaching custom
# handlers to the "unreturned_error" signal. Thus the last arg to
# GConfClient functions is None.
#

# Special mention of an idiom often used in GTK+ apps that does
# not work right with GConf but may appear to at first:
#
# i_am_changing_value = True
# change_value (value)
# i_am_changing_value = False
# 
# This breaks for several reasons: notification of changes
# may be asynchronous, you may get notifications that are not
# caused by change_value () while change_value () is running,
# since GConf will enter the main loop, and also if you need
# this code to work you are probably going to have issues
# when someone other than yourself sets the value.
# 
# A robust solution in this case is often to compare the old
# and new values to see if they've really changed, thus avoiding
# whatever loop you were trying to avoid.
#

import gconf
import gobject
import gtk

class GConfigExample:
    def __init__(self):
        # Get the default client
        client = gconf.client_get_default()

        # Tell GConfClient that we're interested in the given directory.
        # This means GConfClient will receive notification of changes
        # to this directory, and cache keys under this directory.
        # So _don't_ add "/" or something silly like that or you'll end
        # up with a copy of the whole GConf database. ;-)
        #
        # We use PRELOAD_NONE to avoid loading all config keys on
        # startup. If your app pretty much reads all config keys
        # on startup, then preloading the cache may make sense.

        client.add_dir ("/apps/pygtk-book-gconf-example-app", gconf.CLIENT_PRELOAD_NONE)
        self.window = gtk.Window ()
        self.window.set_title ('GConfig Example')
      
        vbox = gtk.VBox (False, 5)
        self.window.add (vbox)
      
        # Create labels that we can "configure"
        config = self.create_configurable_widget (client, "/apps/pygtk-book-gconf-example-app/foo")
        vbox.pack_start (config, True, True)

        config = self.create_configurable_widget (client, "/apps/pygtk-book-gconf-example-app/bar")
        vbox.pack_start (config, True, True)
      
        config = self.create_configurable_widget (client, "/apps/pygtk-book-gconf-example-app/baz")
        vbox.pack_start (config, True, True)

        config = self.create_configurable_widget (client, "/apps/pygtk-book-gconf-example-app/blah")
        vbox.pack_start (config, True, True)

        self.window.connect ('delete_event', lambda wid, we: gtk.main_quit())
        self.window.set_data ('client', client)
      
        prefs_button = gtk.Button ("Preferences")
        vbox.pack_end (prefs_button, False, False)
        prefs_button.connect ('clicked', self.prefs_button_clicked_callback)
        self.window.show_all()
    
    
    # Remove the notification callback when the widget monitoring
    # notifications is destroyed
    def configurable_widget_destroy_callback (self, widget):
        client = widget.get_data('client')
        notify_id = widget.get_data('notify_id')

        if notify_id:
            client.notify_remove (notify_id)

    # Notification callback for our label widgets that
    # monitor the current value of a gconf key. i.e.
    # we are conceptually "configuring" the label widgets
    def configurable_widget_config_notify (self, client, cnxn_id, entry, label):
        
        # Note that value can be None (unset) or it can have
        # the wrong type! Need to check that to survive
        # gconftool --break-key
      
        if not entry.value:
            label.set_text ('')
        elif entry.value.type == gconf.VALUE_STRING:
            label.set_text (entry.value.to_string ())
        else:
            label.set_text ('!type error!')

    # Create a GtkLabel inside a frame, that we can "configure"
    # (the label displays the value of the config key).
    def create_configurable_widget (self, client, config_key):
        hbox = gtk.HBox(True)
        key_label = gtk.Label(config_key + ": ")
        
        label = gtk.Label ('')
        hbox.pack_start(key_label)
        hbox.pack_start(label)
      
        s = client.get_string(config_key)

        if s:
            label.set_text(s)

        notify_id = client.notify_add (config_key, self.configurable_widget_config_notify, label)

        # Note that notify_id will be 0 if there was an error,
        # so we handle that in our destroy callback.
      
        label.set_data ('notify_id', notify_id)
        label.set_data ('client', client)
        label.connect ('destroy', self.configurable_widget_destroy_callback)
        
        return hbox

    # prefs button clicked 
    def prefs_button_clicked_callback(self, widget):
        client = self.window.get_data ('client')
        prefs_dialog = EditConfigValues(client)

#
# Preferences dialog code. NOTE that the prefs dialog knows NOTHING
# about the existence of the main window; it is purely a way to fool
# with the GConf database. It never does something like change
# the main window directly; it ONLY changes GConf keys via
# GConfClient. This is _important_, because people may configure
# your app without using your preferences dialog.
#
# This is an instant-apply prefs dialog. For a complicated
# apply/revert/cancel dialog as in GNOME 1, see the
# complex-gconf-app.c example. But don't actually copy that example
# in GNOME 2, thanks. ;-) complex-gconf-app.c does show how
# to use GConfChangeSet.
#

class EditConfigValues:
    def __init__(self, client):
        self.dialog = gtk.Dialog ("GConfig Example Preferences",
                             None, 0, (gtk.STOCK_CLOSE, gtk.RESPONSE_ACCEPT))

        # destroy dialog on button press
        self.dialog.connect ('response', lambda wid,ev: wid.destroy ())

        self.dialog.set_default_response (gtk.RESPONSE_ACCEPT)

        vbox = gtk.VBox (False, 5)
      
        self.dialog.vbox.pack_start (vbox)

        entry = self.create_config_entry (client, "/apps/pygtk-book-gconf-example-app/foo", True)
        vbox.pack_start (entry, False, False)

        entry = self.create_config_entry (client, "/apps/pygtk-book-gconf-example-app/bar")
        vbox.pack_start (entry, False, False)
      
        entry = self.create_config_entry (client, "/apps/pygtk-book-gconf-example-app/baz")
        vbox.pack_start (entry, False, False)

        entry = self.create_config_entry (client, "/apps/pygtk-book-gconf-example-app/blah")
        vbox.pack_start (entry, False, False)

        self.dialog.show_all()

    # Commit changes to the GConf database. 
    def config_entry_commit (self, entry, *args):
        client = entry.get_data ('client')
        text = entry.get_chars (0, -1)

        key = entry.get_data ('key')

        # Unset if the string is zero-length, otherwise set
        if text:
            client.set_string (key, text)
        else:
            client.unset (key)
        
    # Create an entry used to edit the given config key 
    def create_config_entry (self, client, config_key, focus=False):
        hbox = gtk.HBox (False, 5)
        label = gtk.Label (config_key)
        entry = gtk.Entry ()

        hbox.pack_start (label, False, False, 0)
        hbox.pack_end (entry, False, False, 0)

        # this will print an error via default error handler
        # if the key isn't set to a string

        s = client.get_string(config_key)
        if s:
	        entry.set_text(s)
      
        entry.set_data ('client', client)
        entry.set_data ('key', config_key)

        # Commit changes if the user focuses out, or hits enter; we don't
        # do this on "changed" since it'd probably be a bit too slow to
        # round-trip to the server on every "changed" signal.

        entry.connect ('focus_out_event', self.config_entry_commit)
        entry.connect ('activate', self.config_entry_commit)    
       
        # Set the entry insensitive if the key it edits isn't writable.
        # Technically, we should update this sensitivity if the key gets
        # a change notify, but that's probably overkill.

        entry.set_sensitive (client.key_is_writable (config_key))

        if focus:
            entry.grab_focus ()
      
        return hbox


if __name__ == "__main__":
    GConfigExample()
    gtk.main()
