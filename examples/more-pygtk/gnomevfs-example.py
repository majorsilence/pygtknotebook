import gtk
import gnomevfs
gnome.ui.authentication_manager_init()
#filechooserdialog.set_current_folder_uri("sftp://user@host/path") 

text_buffer=None

def read_vfs_dir(self):
    print "OpenFile.read_files"
    dh = gnomevfs.DirectoryHandle(self.dir)
    for x in dh:
        print x

def read_vfs_files(self):
    print "OpenFile.read_files()"
    for x in self.files:
        file = gnomevfs.URI(x)
        print file
        text_buffer.insert(line)
        
def main():
    global text_buffer
    win = gtk.Window()
    vbox = gtk.VBox()
    hbox = gtk.HBox()
    
    location = gt.Entry("")
    read_text = gtk.Button("Read Text")
    text = gtk.TextView()
    text_buffer = text.get_buffer()
    
    vbox.pack_start(read_text, False, True, 0)
    vbox.pack_start(location, False, True, 0)
    vbox.pack_start(text, False, True, 0)
    
    win.add(vbox)
    win.show_all()
    gtk.main()
