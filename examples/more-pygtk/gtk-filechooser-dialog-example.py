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
    window.set_title("Filechooser Example")

    window.connect("destroy", lambda wid: gtk.main_quit())
    window.connect("delete_event", lambda a1,a2:gtk.main_quit())

    button_save = gtk.Button("Save File")
    button_open = gtk.Button("Open File")
    
    button_save.connect("clicked", on_save_clicked, text_filter, all_filter)
    button_open.connect("clicked", on_open_clicked, text_filter, all_filter)
    
    hbox = gtk.HBox(True, 0)
    hbox.pack_start(button_save, True, True, 5)
    hbox.pack_start(button_open, True, True, 5)   

    window.add(hbox)
    window.show_all()


def on_save_clicked(widget, text_filter=None, all_filter=None):
    filename=None
    dialog=gtk.FileChooserDialog(title="Select a File", action=gtk.FILE_CHOOSER_ACTION_SAVE,
        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
      
    if (text_filter != None) and (all_filter != None):
        dialog.add_filter(text_filter)
        dialog.add_filter(all_filter)
        
    response = dialog.run()
            
    if response == gtk.RESPONSE_OK:
        filename = dialog.get_filename()
    elif response == gtk.RESPONSE_CANCEL:
        print 'Cancel Clicked'
    dialog.destroy()
    
    if filename != None:
        save_file=open(filename, 'w')
        save_file.write("Sample Data")
        save_file.close()
    print "File Saved: ", filename

def on_open_clicked(widget, text_filter=None, all_filter=None):
    filename=None
    dialog=gtk.FileChooserDialog(title="Select a File", action=gtk.FILE_CHOOSER_ACTION_OPEN,
        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    if (text_filter != None) and (all_filter != None):
        dialog.add_filter(text_filter)
        dialog.add_filter(all_filter)
    
    response = dialog.run()
            
    if response == gtk.RESPONSE_OK:
        filename = dialog.get_filename()
    elif response == gtk.RESPONSE_CANCEL:
        print 'Cancel Clicked'
    dialog.destroy()
    
    print "File Choosen: ", filename
   
if __name__ == "__main__":
    main()
    gtk.main()

    
