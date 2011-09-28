import clr
clr.AddReference('gtk-sharp')
import Gtk

class GtkExample(object):
	def __init__(self):
		Gtk.Application.Init()
		
		self.window = Gtk.Window("Hello World")
		self.window.DeleteEvent += self.DeleteEvent
		
		vbox = Gtk.VBox() 
		
		button = Gtk.Button("Show Message")
		button.Clicked += self.HelloWorld
		
		self.textentry1 = Gtk.Entry("Default Text")
		
		vbox.PackStart(self.textentry1)
		vbox.PackStart(button)
		
		self.window.Add(vbox)
		self.window.ShowAll()
		Gtk.Application.Run()

	def DeleteEvent(self, widget, event):
		Gtk.Application.Quit()
		
	def HelloWorld(self, widget, event):
		m = Gtk.MessageDialog(None, Gtk.DialogFlags.Modal, Gtk.MessageType.Info, \
			Gtk.ButtonsType.YesNo, False, 'Change the text entry to "Hello World?"')

		result = m.Run()
		m.Destroy()
		if result == int(Gtk.ResponseType.Yes):
			self.textentry1.Text = "Hello World!"
		
	
if __name__ == "__main__":
	GtkExample()
