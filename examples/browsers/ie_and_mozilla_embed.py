"""Embedding IE in pygtk via AtlAxWin and ctypes."""
# needs the comtypes package from http://sourceforge.net/projects/comtypes/

import sys

import pygtk
pygtk.require("2.0")
import gtk

if sys.platform=="win32":
    import win32con

    from ctypes import *
    from ctypes.wintypes import *
    from comtypes import IUnknown
    from comtypes.automation import IDispatch, VARIANT
    from comtypes.client import wrap

    kernel32 = windll.kernel32
    user32 = windll.user32
    atl = windll.atl
else:
    import gtkmozembed
    
class GUI:
    def __init__(self):
        self.home_url = "http://www.majorsilence.com/"
    
        # Create the main GTK window.
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.set_title("Example Webbrowser that works on Linux and Windows")
        self.win.connect("destroy", gtk.main_quit)
        self.win.set_size_request(750, 550)
        self.win.realize()
        
        # Create a VBox to house the address bar and the IE control.
        self.main_vbox = gtk.VBox()


        # ####
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

        back.connect("clicked", self.on_backward_clicked, None)
        forward.connect("clicked", self.on_forward_clicked, None)
        refresh.connect("clicked", self.on_refresh_clicked, None)
        stop.connect("clicked", self.on_stop_clicked, None)
        home.connect("clicked", self.on_home_clicked, None)
        
        self.address.connect("key_press_event", self.on_address_keypress)
        go.connect("clicked", self.on_go_clicked, None)

        self.main_vbox.pack_start(control_box, False, True, 2)
        
        # ######
        
         
        # show the main window
        self.win.add(self.main_vbox)
        self.win.show_all()
         
        if sys.platform=="win32":
            self.init_ie()
        else:
            self.init_mozilla()
    
    def init_ie(self):
    
        # Create a DrawingArea to host IE and add it to the hbox.
        self.container = gtk.DrawingArea()
        self.main_vbox.add(self.container)
        self.container.show()
        
        # Make the container accept the focus and pass it to the control;
        # this makes the Tab key pass focus to IE correctly.
        self.container.set_property("can-focus", True)
        self.container.connect("focus", self.on_container_focus)
        
        # Resize the AtlAxWin window with its container.
        self.container.connect("size-allocate", self.on_container_size)
        
        # Create an instance of IE via AtlAxWin.
        atl.AtlAxWinInit()
        hInstance = kernel32.GetModuleHandleA(None)
        parentHwnd = self.container.window.handle
        self.atlAxWinHwnd = user32.CreateWindowExA(0, "AtlAxWin", self.home_url,
                            win32con.WS_VISIBLE | win32con.WS_CHILD |
                            win32con.WS_HSCROLL | win32con.WS_VSCROLL,
                            0, 0, 100, 100, parentHwnd, None, hInstance, 0)
        
        # Get the IWebBrowser2 interface for the IE control.
        pBrowserUnk = POINTER(IUnknown)()
        atl.AtlAxGetControl(self.atlAxWinHwnd, byref(pBrowserUnk))
        # the wrap call querys for the default interface
        self.browser = wrap(pBrowserUnk)
        
        # Create a Gtk window that refers to the native AtlAxWin window.
        self.gtkAtlAxWin = gtk.gdk.window_foreign_new(long(self.atlAxWinHwnd))

        # By default, clicking a GTK widget doesn't grab the focus away from
        # a native Win32 control.
        self.address.connect("button-press-event", self.on_widget_click)
        
    def init_mozilla(self):
        self.browser = gtkmozembed.MozEmbed()
        self.main_vbox.add(self.browser)
        self.browser.load_url(self.home_url)
    
    def on_backward_clicked(self, widget=None, data=None):
        if sys.platform=="win32":
            try:
                self.browser.GoBack()
            except:
                pass # No page to go back to
        else:
            if self.browser.can_go_back():
                self.browser.go_back()
        
    def on_forward_clicked(self, widget=None, data=None):
        if sys.platform=="win32":
            try:
                self.browser.GoForward()
            except:
                pass
        else:
            if self.browser.can_go_forward():
                self.browser.go_forward()
        
    def on_refresh_clicked(self, widget=None, data=None):
        if sys.platform=="win32":
            self.browser.Refresh()
        else:
            self.browser.reload(gtkmozembed.FLAG_RELOADNORMAL)
        
    def on_stop_clicked(self, widget=None, data=None):
        if sys.platform=="win32":
            self.browser.Stop()
        else:
            self.browser.stop_load()
        
    def on_home_clicked(self, widget=None, data=None):
        if sys.platform=="win32":
            # To go to Internet explorer's default home page use the browser.GoHome()
            #self.browser.GoHome()
            v = byref(VARIANT())
            self.browser.Navigate(self.home_url, v, v, v, v)
        else:
            self.browser.load_url(self.home_url)  
                
    def on_go_clicked(self, widget=None, data=None):
        if sys.platform=="win32":
            v = byref(VARIANT())
            self.browser.Navigate(self.address.get_text(), v, v, v, v)
            #print dir(self.browser)
        else:
            self.browser.load_url(self.address.get_text())
    
    def on_address_keypress(self, widget, event):
        #print "Key event in address bar"
        if gtk.gdk.keyval_name(event.keyval) == "Return":
            print "Key press: Return"
            self.on_go_clicked(None)
    
    def on_widget_click(self, widget, data):
        # used on win32 platform because by default a gtk application does not grab control from native win32 control
        self.win.window.focus()
        
    def on_container_size(self, widget, sizeAlloc):
        self.gtkAtlAxWin.move_resize(0, 0, sizeAlloc.width, sizeAlloc.height)

    def on_container_focus(self, widget, data):
        # Used on win32 with Internet Explorer
        # Pass the focus to IE.  First get the HWND of the IE control; this
        # is a bit of a hack but I couldn't make IWebBrowser2._get_HWND work.
        rect = RECT()
        user32.GetWindowRect(self.atlAxWinHwnd, byref(rect))
        ieHwnd = user32.WindowFromPoint(POINT(rect.left, rect.top))
        user32.SetFocus(ieHwnd)

if "__name__" == "__main__":
    gui = GUI()
    gtk.main()



