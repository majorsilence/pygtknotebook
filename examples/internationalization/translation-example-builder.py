import pygtk
pygtk.require("2.0")
import gtk
import locale
import gettext


APP="translation-example"
DIR="po-glade"

locale.setlocale(locale.LC_ALL, '')
# This is needed to make gtk.Builder work by specifying the 
# translations directory
locale.bindtextdomain(APP, DIR)

gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
lang = gettext.translation(APP, DIR)
_ = lang.gettext
gettext.install(APP, DIR)

class TranslationExample(object):
    def on_button_clicked(self, widget, data=None):
        self.label_1.set_text( _("Hello ") + str(data) )

    def __init__(self):
        self.gladefile = gtk.Builder()
        self.gladefile.set_translation_domain(APP)
        self.gladefile.add_from_file("translation-example.xml")
        
        self.gladefile.connect_signals(self)
        self.main_window = self.gladefile.get_object("window1")
        self.main_window.connect("delete_event", lambda wid, we: gtk.main_quit()) 
        self.main_window.show_all()

if __name__ == "__main__":
    TranslationExample()
    gtk.main() 
