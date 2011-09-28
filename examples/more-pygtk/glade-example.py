import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

class GladeExample(object):
    def __init__(self):
        self.gladefile = gtk.glade.XML("glade-example.glade")
        self.gladefile.signal_autoconnect(self)
        self.main_window = self.gladefile.get_widget("window1")
        self.about_dialog = self.gladefile.get_widget("aboutdialog1")
        self.message_dialog = self.gladefile.get_widget("messagedialog1")
        
    def on_about_clicked(self, widget):
        print "on_about_clicked"
        # The main window would not likely be hidden in a real application
        # just to show an about dialog.
        self.main_window.hide()
        self.about_dialog.run()
        self.about_dialog.destroy()
        self.main_window.show()

    def on_message_clicked(self, widget):
        print "on_message_clicked"
        # The main window would not likely be hidden in a real application
        # just to show an about dialog.
        self.main_window.hide()
        self.message_dialog.run()
        self.message_dialog.destroy()
        self.main_window.show()

    def on_window1_delete_event(self, widget, event):
        gtk.main_quit()
        
if __name__ == "__main__":
    app = GladeExample()
    gtk.main()

