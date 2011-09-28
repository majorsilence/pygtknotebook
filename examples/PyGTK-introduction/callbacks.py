import pygtk
pygtk.require("2.0")
import gtk

def on_button_clicked(widget, data=None):
    label_1.set_text("Hello " + str(data))

label_1 = gtk.Label("Hello World!")
label_2 = gtk.Label("Still in the HBox")
button = gtk.Button("Click Me")

#Connect the "clicked" signal of the button to our callback function that we have named on_button_clicked
# It also passes the string "Anything can go here" to the callback function.
button.connect("clicked", on_button_clicked, "Anything can go here")

vbox = gtk.VBox()

vbox.pack_start(label_1)
vbox.pack_start(label_2)
vbox.pack_start(button)

win = gtk.Window()
win.connect("destroy", lambda wid: gtk.main_quit())
win.add(vbox)
win.show_all()
gtk.main() 