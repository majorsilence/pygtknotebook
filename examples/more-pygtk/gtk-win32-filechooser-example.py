import pygtk
pygtk.require('2.0')
import gtk
import os
import win32gui, win32con
    
def main():
    file_filter="""Text files\0*.txt\0All Files\0*.*\0"""
    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title("Windows Filechooser Example")

    window.connect("destroy", lambda wid: gtk.main_quit())
    window.connect("delete_event", lambda e1,e2:gtk.main_quit())

    button_save = gtk.Button("Save File")
    button_open = gtk.Button("Open File")
    
    button_save.connect("clicked", on_save_clicked, file_filter)
    button_open.connect("clicked", on_open_clicked, file_filter)
    
    hbox = gtk.HBox(True, 0)
    hbox.pack_start(button_save, True, True, 5)
    hbox.pack_start(button_open, True, True, 5)   

    window.add(hbox)
    window.show_all()

def on_save_clicked(widget, file_filter=None):
    filename=None
    try:
        filename, customfilter, flags=win32gui.GetSaveFileNameW(
            InitialDir=os.path.join(os.environ['USERPROFILE'],"My Documents"),
            Flags=win32con.OFN_ALLOWMULTISELECT|win32con.OFN_EXPLORER,
            File='', DefExt='txt',
            Title='Save a File',
            Filter=file_filter,
            FilterIndex=0)
    except win32gui.error:
        print "Cancel clicked"
    print filename
    if filename != None:
        save_file = open(filename, 'w')
        save_file.write("Test Save Data")
        save_file.close()
    return filename

def on_open_clicked(widget, file_filter=None):
    filename=None
    try:
        filename, customfilter, flags=win32gui.GetOpenFileNameW(
            InitialDir=os.path.join(os.environ['USERPROFILE'],"My Documents"),
            Flags=win32con.OFN_ALLOWMULTISELECT|win32con.OFN_EXPLORER,
            File='', DefExt='txt',
            Title='Select a File',
            Filter=file_filter,
            FilterIndex=0)
    except win32gui.error:
        print "Cancel clicked"
    
    print 'open file names:', filename
    return filename
  
if __name__ == "__main__":
    main()
    gtk.main()
    
