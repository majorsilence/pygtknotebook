#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk


class ComboExample:
    def __init__(self):
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.connect("delete_event", lambda wid, we: gtk.main_quit())
        vbox = gtk.VBox(True, 2)
        win.add(vbox)

        default_items = ["hello", "World"]
        self.item_list = gtk.combo_box_entry_new_text()
        self.item_list.child.connect('key-press-event', self.item_list_changed)
        for x in default_items:
            self.item_list.append_text(x)

        vbox.pack_start(self.item_list, True, True, 2)

        button = gtk.Button("Print Selected Item")
        button.connect("clicked", self.print_selected_item)
        vbox.pack_start(button, True, True, 2)

        win.show_all()


    def item_list_changed(self, widget=None, event=None):
        key = gtk.gdk.keyval_name(event.keyval)
        if key == "Return":
            self.item_list.append_text(widget.get_text())
            widget.set_text("")

    def print_selected_item(self, widget=None):
        model = self.item_list.get_model()
        active = self.item_list.get_active()
        if active < 0:
            return None
        print model[active][0]
        return model[active][0]


if __name__ == "__main__":
    ComboExample()
    gtk.main()
