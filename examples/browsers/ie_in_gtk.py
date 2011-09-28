"""A poor man's webbrowser, embedding IE in pygtk via AtlAxWin and ctypes."""
# needs the comtypes package from http://sourceforge.net/projects/comtypes/

import win32con

from ctypes import *
from ctypes.wintypes import *
from comtypes import IUnknown
from comtypes.automation import IDispatch, VARIANT
from comtypes.client import wrap

kernel32 = windll.kernel32
user32 = windll.user32
atl = windll.atl                  # If this fails, you need atl.dll

import pygtk
pygtk.require("2.0")
import gtk

class GUI:
    def __init__(self):
        # Create the main GTK window.
        self.main = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main.set_title("Poor man's browser [TM]")
        self.main.connect("destroy", gtk.main_quit)
        self.main.set_size_request(750, 550)
        self.main.realize()
        
        # Create a VBox to house the address bar and the IE control.
        self.mainVBox = gtk.VBox()
        self.main.add(self.mainVBox)
        self.mainVBox.show()
        
        # Create the address bar.
        self.addressEntry = gtk.Entry()
        self.addressEntry.show()
        self.addressEntry.connect("key-press-event", self.on_addressEntry_key)
        self.addressLabel = gtk.Label()
        self.addressLabel.set_text_with_mnemonic("_Address: ")
        self.addressLabel.set_mnemonic_widget(self.addressEntry)
        self.addressLabel.show()
        self.goButton = gtk.Button("  Go  ")
        self.goButton.show()
        self.goButton.connect("clicked", self.on_goButton_clicked)
        self.addressHbox = gtk.HBox()
        self.addressHbox.show()
        self.addressHbox.add(self.addressLabel)
        self.addressHbox.add(self.addressEntry)
        self.addressHbox.add(self.goButton)
        self.addressHbox.set_child_packing(self.addressLabel,
                                           False, True, 2, gtk.PACK_START)
        self.addressHbox.set_child_packing(self.goButton,
                                           False, True, 0, gtk.PACK_END)
        self.mainVBox.add(self.addressHbox)
        self.mainVBox.set_child_packing(self.addressHbox,
                                        False, True, 0, gtk.PACK_START)
        
        # Create a DrawingArea to host IE and add it to the hbox.
        self.container = gtk.DrawingArea()
        self.mainVBox.add(self.container)
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
        self.atlAxWinHwnd = \
            user32.CreateWindowExA(0, "AtlAxWin", "http://www.pygtk.org",
                            win32con.WS_VISIBLE | win32con.WS_CHILD |
                            win32con.WS_HSCROLL | win32con.WS_VSCROLL,
                            0, 0, 100, 100, parentHwnd, None, hInstance, 0)
        
        # Get the IWebBrowser2 interface for the IE control.
        pBrowserUnk = POINTER(IUnknown)()
        atl.AtlAxGetControl(self.atlAxWinHwnd, byref(pBrowserUnk))
        # the wrap call querys for the default interface
        self.pBrowser = wrap(pBrowserUnk)
        
        # Create a Gtk window that refers to the native AtlAxWin window.
        self.gtkAtlAxWin = gtk.gdk.window_foreign_new(long(self.atlAxWinHwnd))

        # By default, clicking a GTK widget doesn't grab the focus away from
        # a native Win32 control.
        self.addressEntry.connect("button-press-event", self.on_widget_click)
    
    def on_goButton_clicked(self, widget):
        v = byref(VARIANT())
        self.pBrowser.Navigate(self.addressEntry.get_text(), v, v, v, v)
    
    def on_addressEntry_key(self, widget, event):
        if event.keyval == 65293:   # "Enter"; is there a constant for this?
            self.on_goButton_clicked(None)
    
    def on_widget_click(self, widget, data):
        self.main.window.focus()
        
    def on_container_size(self, widget, sizeAlloc):
        self.gtkAtlAxWin.move_resize(0, 0, sizeAlloc.width, sizeAlloc.height)

    def on_container_focus(self, widget, data):
        # Pass the focus to IE.  First get the HWND of the IE control; this
        # is a bit of a hack but I couldn't make IWebBrowser2._get_HWND work.
        rect = RECT()
        user32.GetWindowRect(self.atlAxWinHwnd, byref(rect))
        ieHwnd = user32.WindowFromPoint(POINT(rect.left, rect.top))
        user32.SetFocus(ieHwnd)

# Show the main window and run the message loop.
gui = GUI()
gui.main.show()
gtk.main()
