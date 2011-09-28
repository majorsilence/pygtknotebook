#!/usr/bin/python

import gtk
import gtkmozembed

class ExampleBrowser(object):
    def __init__(self):
        data = """<html><head><title>Hello</title></head>
        <body>
        PyGTK using MozEmbed to embed a web browser.
        </body>
        </html>"""
      
        win = gtk.Window()
        win.set_size_request(800, 600)
        win.connect("delete_event", lambda w,e: gtk.main_quit())
        
        # gtk.VBox(homogeneous=False, spacing=0)
        vbox = gtk.VBox(False, 0)
        control_box = gtk.HBox(False, 0)
        
        #pack_start(button, expand, fill, padding)
        back = gtk.Button("Back")
        forward = gtk.Button("Forward")
        refresh = gtk.Button("Refresh")
        stop = gtk.Button("Stop")
        home = gtk.Button("Home")
        self.address = gtk.Entry(max=0) # no limit on address length
        go = gtk.Button("Go")
        
        control_box.pack_start(back, True, True, 2)
        control_box.pack_start(forward, True, True, 2)
        control_box.pack_start(refresh, True, True, 2)
        control_box.pack_start(stop, True, True, 2)
        control_box.pack_start(home, True, True, 2)
        control_box.pack_start(self.address, True, True, 2)
        control_box.pack_start(go, True, True, 2)

        back.connect("clicked", self.on_back_clicked, None)
        forward.connect("clicked", self.on_forward_clicked, None)
        refresh.connect("clicked", self.on_refresh_clicked, None)
        stop.connect("clicked", self.on_stop_clicked, None)
        home.connect("clicked", self.on_home_clicked, data)
        self.address.connect("key_press_event", self.on_address_keypress)
        go.connect("clicked", self.on_go_clicked, None)

        vbox.pack_start(control_box, False, True, 2)
        
        self.browser = gtkmozembed.MozEmbed()
        #gtkmozembed.set_profile_path("/tmp", "foobar")
        vbox.add(self.browser)
        win.add(vbox)
        win.show_all()
        
        ## self.browser.load_url('http://www.pygtk.org')
        self.browser.render_data(data, long(len(data)), 'file:///', 'text/html')
       
        # Load file from file system
        #self.browser.load_url('file:///path/to/file/name.html')

    def on_back_clicked(self, widget=None, data=None):
        print "Back button clicked."
        if self.browser.can_go_back():
            self.browser.go_back()

    def on_forward_clicked(self, widget=None, data=None):
        print "Forward button clicked."
        if self.browser.can_go_forward():
            self.browser.go_forward()

    def on_refresh_clicked(self, widget=None, data=None):
        print "Refresh button clicked."
        self.browser.reload(gtkmozembed.FLAG_RELOADNORMAL)

    def on_stop_clicked(self, widget=None, data=None):
        print "Stop Button Clicked."
        self.browser.stop_load()

    def on_home_clicked(self, widget=None, data=None):
        print "Home Button clicked."
        print "Back button only works on actual pages and not render_data"
        self.browser.render_data(data, long(len(data)), 'file:///', 'text/html')
    
    def on_address_keypress(self, widget, event):
        print "Key event in address bar"
        if gtk.gdk.keyval_name(event.keyval) == "Return":
            print "Key press: Return"
            self.on_go_clicked(None)

    def on_go_clicked(self, widget=None, data=None):
        print "Go Button Clicked."
        self.browser.load_url(self.address.get_text())

if __name__ == '__main__':
    ExampleBrowser()
    gtk.main()
