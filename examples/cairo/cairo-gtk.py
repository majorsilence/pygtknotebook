#!/usr/bin/env python
import gtk
import cairo
import math


class CairoGtkOverride(gtk.DrawingArea):
    """
    Class that demonstrates how to do custom widgets overriding the expose_event signal
    """
    # override
    __gsignals__ = {"expose_event": "override" } # do_expose_event(self, event)
    # see: http://www.sicem.biz/personal/lgs/docs/docs/gobject-python/gobject-tutorial.html#d0e570

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        
    def do_expose_event(self, event):
        # Create the cairo context
        context = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        context.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        context.clip()

        print self.window.get_size()
        self.draw(context, *self.window.get_size())
    
    def draw(self, context, width, height):
        print "CairoGtk draw"
        # Fill the background with red
        context.set_source_rgb(0.5, 0.0, 0.0)
        context.rectangle(0, 0, width, height)
        context.fill()

class CairoGtkConnect(gtk.DrawingArea):
    """
    Class that demonstrates how to create a custom widget by connecting to the expose_event signal.
    """
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        #connect
        self.connect("expose_event", self.do_expose_event)
        
    def do_expose_event(self, widget, event):
        # Create the cairo context
        context = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        context.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        context.clip()

        self.draw(context, *self.window.get_size())
        # other option is to use get_allocation in the draw methods to retrieve the size
        # but that would require doing so in every subclass
        # rect = self.get_allocation()
        # width = rect.width
        # height = rect.height
    
    def draw(self, context, width, height):
        print "CairoGtk draw"
        # Fill the background with blue
        context.set_source_rgb(0.0, 0.0, 0.5)
        context.rectangle(0, 0, width, height)
        context.fill()

class Circle(CairoGtkOverride):
    """
    Class extends one of the custom widgets to draw something other than the default custom widget
    """
    def draw(self, context, width, height):
        # And a circle
        print "Circle draw"
        context.set_source_rgb(1.0, 0.0, 0.0)
        radius = min(width, height)
        context.arc(width / 2.0, height / 2.0, radius / 2.0 - 20, 0, 2 * math.pi)
        context.stroke()

if __name__ == "__main__":
    win = gtk.Window()
    win.connect("delete-event", gtk.main_quit)
    
    vbox = gtk.VBox()
    
    override_widget = CairoGtkOverride()
    connect_widget = CairoGtkConnect()
    circle_widget = Circle()
    
    vbox.pack_start(override_widget, True, True, 0)
    vbox.pack_start(connect_widget, True, True, 0)
    vbox.pack_start(circle_widget, True, True, 0)
    
    win.add(vbox)
    win.show_all()

    gtk.main()


