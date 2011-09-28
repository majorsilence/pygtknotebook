import pygtk
pygtk.require('2.0')
import gtk

def main():
    #file filters used with the filechoosers
    text_filter=gtk.FileFilter()
    text_filter.set_name("Text files")
    text_filter.add_mime_type("text/*")
    all_filter=gtk.FileFilter()
    all_filter.set_name("All files")
    all_filter.add_pattern("*")

    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title("Native Filechooser")

    window.connect("destroy", lambda wid: gtk.main_quit())
    window.connect("delete_event", lambda e1,e2:gtk.main_quit())

    button_open = gtk.FileChooserButton("Open File")
    button_open.add_filter(text_filter)
    button_open.add_filter(all_filter)
    button_open.connect("selection-changed", on_file_selected)

    window.add(button_open)
    window.show_all()

def on_file_selected(widget):
    filename= widget.get_filename()
    print "File Choosen: ", filename
   
if __name__ == "__main__":
    main()
    gtk.main()

