# The term selection target is somewhat misleading. What selection target actually means is the data's format type (i.e. gtk.gdk.Atom, integer, or string) that is being sent or received.

import pygtk
import gtk
import sys
import os

class DragDropExample:

    def __init__(self):
        TARGET_STRING = 82
        TARGET_IMAGE = 83
        self.file_list=[] # list to hold our images
        self.accepted_types = ["jpg", "jpeg", "png", "gif", "bmp"]
        
        win = gtk.Window()
        win.set_size_request(400, 400)
        win.connect("delete_event", lambda w,e: gtk.main_quit())
        
        vbox = gtk.VBox(False, 0)
        hello = gtk.Label("Test label to drag images to.")
        vbox.pack_start(hello, True, True, 0)
        win.add(vbox)
        # Taken from the pygtk tutorial found at:
        # http://www.pygtk.org/pygtktutorial/pygtk2tutorial/sec-DNDMethods.html
        # gtk.DEST_DEFAULT_MOTION:	
        # If set for a widget, GTK+, during a drag over this widget will 
        # check if the drag matches this widget's list of possible targets 
        # and actions. GTK+ will then call drag_status() as appropriate.
        
        # gtk.DEST_DEFAULT_HIGHLIGHT:
        # If set for a widget, GTK+ will draw a highlight on this widget as
        # long as a drag is over this widget and the widget drag format and 
        # action is acceptable.

        # gtk.DEST_DEFAULT_DROP	
        #If set for a widget, when a drop occurs, GTK+ will check if the 
        #drag matches this widget's list of possible targets and actions. 
        #If so, GTK+ will call drag_get_data() on behalf of the widget. 
        #Whether or not the drop is succesful, GTK+ will call drag_finish(). 
        #If the action was a move and the drag was succesful, then TRUE will 
        #be passed for the delete parameter to drag_finish().
        
        #gtk.DEST_DEFAULT_ALL:	
        #If set, specifies that all default actions should be taken.

        if sys.platform=="win32":
            # gtk.DEST_DEFAULT_DROP, does not work on windows because will not match list of possible target matches
            # if you set anything besides a blank [] for target on microsoft windows, it will not call drop_data_received
            # So might as well leave like so and do your own detecting of the files and what to do with it in drag_data_received.
            # must connect to drag_cb on windows, does not matter on linux.
            win.drag_dest_set(0, [], 0)
        else:
            win.drag_dest_set(gtk.DEST_DEFAULT_DROP, [("text/plain", 0, TARGET_STRING), ("image/*", 0, TARGET_IMAGE)], gtk.gdk.ACTION_COPY)
        
        win.connect('drag_motion', self.motion_cb)
        win.connect('drag_drop', self.drop_cb)
        win.connect('drag_data_received', self.drag_data_received)
        
        win.show_all()

    def motion_cb(self, wid, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drop_cb(self, wid, context, x, y, time):
        print 'drop'
        if context.targets:
            wid.drag_get_data(context, context.targets[0], time)
            print "" .join([str(t) for t in context.targets])
            return True
        return False
        
    def drag_data_received(self, img, context, x, y, data, info, time):
        if data.format == 8:
            print "Received %s" % data.data

            # Checking for valid file types
            test_data = os.path.splitext(data.data)[1][1:4].lower().strip()                        
            if test_data  in self.accepted_types:          
                if sys.platform=="win32":
                    # Remove the file:/// on window systems.
                    self.file_list.append(data.data[8:])
                    print data.data[8:]
                else:
                    # Remove the file:// on linux systems.
                    self.file_list.append(data.data[7:])
                    print data.data[7:]          
            context.finish(True, False, time)
        else:
            context.finish(False, False, time)



if __name__ == "__main__":
    DragDropExample()
    gtk.main()


# For more on drag and drop visit the pygtk tutorial page
# at http://www.pygtk.org/pygtktutorial/pygtk2tutorial/sec-DNDMethods.html
# or download pygtk source code and view the demo code.
