import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import locale
import gettext


APP="translation-example"
DIR="po-glade"

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
lang = gettext.translation(APP, DIR)
_ = lang.gettext
gettext.install(APP, DIR)

class TranslationExample(object):
    def on_button_clicked(self, widget, data=None):
        self.label_1.set_text( _("Hello ") + str(data) )

    def __init__(self):
        self.gladefile = gtk.glade.XML("translation-example.glade")
        gtk.glade.bindtextdomain(APP, DIR)
        self.gladefile.signal_autoconnect(self)
        self.main_window = self.gladefile.get_widget("window1") 
        self.main_window.connect("delete_event", lambda wid, we: gtk.main_quit()) 
        self.main_window.show_all()

if __name__ == "__main__":
    TranslationExample()
    gtk.main() 
