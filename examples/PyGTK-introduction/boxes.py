import pygtk
pygtk.require("2.0")
import gtk

label_1 = gtk.Label("Hello World!")
label_2 = gtk.Label("Still in the HBox")
button = gtk.Button("This button is in the Vertical Box")
#hbox = gtk.HBox(homogeneous=False, spacing=0) 
# homogeneous  is whether each object in the box has the same size
# You can have a vertical box (gtk.VBox) or a horizontal box (gtk.HBox).
# Boxes can also be added inside of other boxes.  This is how in PyGTK a program has its layout.
# Take some time and experiment using them.  (I also recommend using Glade 3 to create your user interfaces instead of doing it by hand)
vbox = gtk.VBox()
hbox = gtk.HBox()
# box.pack_start(child, expand=True, fill=True, padding=0)
# Child is the widget you are adding to the box.
# Expand argument is whether to fill the extra space in the box (gtk.HBox or gtk.VBox)
# Fill argument only has an effect if the expand argument is set to True.
# You have the option of using pack_start which adds the widget to the beginning of the box, or pack_end which appends the widget to the end of the box.

hbox.pack_start(label_1)
hbox.pack_start(label_2)

# Add the hbox as the first item in the vertical box that was created above
vbox.pack_start(hbox)
# Add the button as the next item in the vertical box.
vbox.pack_start(button)

win = gtk.Window()
win.connect("destroy", lambda wid: gtk.main_quit())
win.add(vbox)
win.show_all()
gtk.main() 