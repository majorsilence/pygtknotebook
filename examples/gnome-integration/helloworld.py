#!/usr/bin/env python
import sys
# Path to other helloworld python modules such as helloworld_message.py
sys.path.append("/usr/local/lib/helloworld") 
# Path to helloworld shared files such as images and documentation
#other_path="/usr/local/share/helloworld

import gtk
import helloworld_message

if __name__ == '__main__':
    win = gtk.Window()
    win.connect("delete_event", lambda w,e: gtk.main_quit())
    
    label = gtk.Label(helloworld_message.message())
    win.add(label)
    
    win.show_all()
    gtk.main()

