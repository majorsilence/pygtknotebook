import pygtk
pygtk.require("2.0")
import gtk
import locale
import gettext


APP="translation-example"
DIR="po"

lang = gettext.translation(APP, DIR)
gettext.install(APP, DIR)

class TranslationExample(object):
    def on_button_clicked(self, widget, data=None):
        self.label_1.set_text( _("Hello ") + str(data) )

    def __init__(self):
        self.label_1 = gtk.Label( _("Hello World!") )
        label_2 = gtk.Label( _("Still in the HBox") )
        button = gtk.Button( _("Click Me") )

        #Connect the "clicked" signal of the button to our callback function that we have named on_button_clicked
        # It also passes the string "Anything can go here" to the callback function.
        button.connect("clicked", self.on_button_clicked, _("Anything can go here") )

        vbox = gtk.VBox()

        vbox.pack_start(self.label_1)
        vbox.pack_start(label_2)
        vbox.pack_start(button)

        win = gtk.Window()
        win.connect("destroy", lambda wid: gtk.main_quit())
        win.add(vbox)
        win.show_all()

if __name__ == "__main__":
    TranslationExample()
    gtk.main() 
