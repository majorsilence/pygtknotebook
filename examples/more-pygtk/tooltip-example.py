import pygtk
import gtk

def on_query_tooltip(widget, x, y, keyboard_tip, tooltip):
    hbox = gtk.HBox()
    label = gtk.Label('Fancy Tooltip with an Image')

    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DND)

    hbox.pack_start(image, False, False, 0)
    hbox.pack_start(label, False, False, 0)

    hbox.show_all()
    tooltip.set_custom(hbox)

    return True

def main():
    win = gtk.Window()
    win.connect("delete_event", lambda w,e: gtk.main_quit())
    vbox = gtk.VBox(False, 0)
    
    # Easy tooltip
    label = gtk.Label("Display Tooltip.")
    label.set_tooltip_text("This is a Tooltip")
    
    # Fancy tooltip
    fancy_label = gtk.Label("A fancy Tooltip")
    fancy_label.props.has_tooltip = True
    fancy_label.connect("query-tooltip", on_query_tooltip)
    
    vbox.pack_start(label, False, False, 5)
    vbox.pack_start(fancy_label, False, False, 5)
    win.add(vbox)
    win.show_all()

if __name__ == "__main__":
    main()
    gtk.main()
