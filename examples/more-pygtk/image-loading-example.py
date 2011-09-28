import pygtk
import gtk

def main():
    win = gtk.Window()
    win.connect("delete_event", lambda w,e: gtk.main_quit())
    vbox = gtk.VBox(False, 0)
    
    # Stock Icon
    image1 = gtk.Image()
    image1.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DND)
    
    # Image from file
    image2 = gtk.Image()
    image2.set_from_file("flower.jpg")
    
    vbox.pack_start(image1, False, False, 5)
    vbox.pack_start(image2, False, False, 5)
    win.add(vbox)
    win.show_all()

if __name__ == "__main__":
    main()
    gtk.main()
