import pygtk
pygtk.require('2.0')
import gtk

class TreeViewExample:
    def __init__(self):
        # Count the items in the item list
        self.counter = 0
        
        self.win = gtk.Window()
        self.win.set_size_request(400, 400)
        self.win.connect("delete_event", lambda w,e: gtk.main_quit())
        
        vbox = gtk.VBox(False, 0)
        hbox = gtk.HBox(False, 0)
        add_button = gtk.Button("Add Item")
        add_button.connect("clicked", self.add_button_clicked)
        
        remove_button = gtk.Button("Remove Item")
        remove_button.connect("clicked", self.remove_button_clicked)
        
    
        # Treeview Stuff
        self.liststore = gtk.ListStore(str, str)
        self.treeview = gtk.TreeView(self.liststore)
        
        # Add cell and column.  Needed to view
        # data added to treeview.
        self.cell = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()
        
        # text=number is the column the text is displayed from
        self.treeviewcolumn = gtk.TreeViewColumn("Button Pushed", self.cell, text=0)
        self.treeviewcolumn2 = gtk.TreeViewColumn("Second Useless Column", self.cell2, text=1)
        
        self.treeview.append_column(self.treeviewcolumn)
        self.treeview.append_column(self.treeviewcolumn2)
        
        vbox.pack_start(self.treeview, True, True, 0)
        vbox.pack_start(hbox, False, True, 0)
        hbox.pack_start(add_button, True, True, 0)
        hbox.pack_start(remove_button, True, True, 0)
        self.win.add(vbox)
        self.win.show_all()

    def add_button_clicked(self, w):
        self.counter += 1
        model = self.treeview.get_model()
        model.append(["Add Button Pushed %s times" % self.counter, "Column 2 Message"])
    
    def remove_button_clicked(self, w):
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            model.remove(iter)
        return    
        
if __name__ == "__main__":
    TreeViewExample()
    gtk.main()
