#!/bin/env python
"""
Based off python example print_editor that comes with pygtk source:
Alexander Larsson (C version)
Gustavo Carneiro (Python translation)
"""
# 1024.0 is float(pango.SCALE)
# Does not work on ubuntu gutsy - blah
# *** glibc detected *** python: corrupted double-linked list: 0x0000000001143e30 ***
# Some in the while loop of the draw_page method messes up
#
# Need to use at least Ubuntu Hardy or Debian Lenny
# as there are to many bugs in older versions

import pygtk
pygtk.require("2.0")
import sys
import math
import cairo
import pango
import gtk

print_text = None

class PrintExample:    
    def __init__(self, action=None, data=None, filename=None):
        self.text = data
        self.layout = None
        self.page_breaks = None
        self.font_size=12
        if action==None:
            # By default set the print action to preview
            action = gtk.PRINT_OPERATION_ACTION_PREVIEW
        
        # Paper Size 
        paper_size = gtk.PaperSize(gtk.PAPER_NAME_A4)
        # Available Papers
        # gtk.PAPER_NAME_A3 - Name for the A4 paper size.
        # gtk.PAPER_NAME_A4 - Name for the A4 paper size.
        # gtk.PAPER_NAME_A5 -Name for the A5 paper size.
        # gtk.PAPER_NAME_B5 -Name for the B5 paper size.
        # gtk.PAPER_NAME_LETTER - Name for the Letter paper size.
        # gtk.PAPER_NAME_EXECUTIVE - Name for the Executive paper size.
        # gtk.PAPER_NAME_LEGAL - for the Legal paper size.
        # Page Setup
        setup = gtk.PageSetup()
        setup.set_paper_size(paper_size)

        
        # PrintOperation
        print_ = gtk.PrintOperation()
        print_.set_default_page_setup(setup)
        print_.set_unit(gtk.UNIT_MM)

        print_.connect("begin_print", self.begin_print)
        print_.connect("draw_page", self.draw_page)
  
        if action == gtk.PRINT_OPERATION_ACTION_EXPORT:
            print_.set_export_filename(filename)
        res = print_.run(action)
    
    def begin_print(self, operation, context):
        width = context.get_width()
        height = context.get_height()
        print height
        self.layout = context.create_pango_layout()
        self.layout.set_font_description(pango.FontDescription("Sans " + str(self.font_size)))
        self.layout.set_width(int(width*pango.SCALE))
        self.layout.set_text(self.text)

        num_lines = self.layout.get_line_count()
        print "num_lines: ", num_lines

        page_breaks = []
        page_height = 0

        for line in xrange(num_lines):
            layout_line = self.layout.get_line(line)
            ink_rect, logical_rect = layout_line.get_extents()
            x_bearing, y_bearing, lwidth, lheight = logical_rect

            line_height = lheight / 1024.0 # 1024.0 is float(pango.SCALE)
            page_height += line_height
            # page_height is the current location on a page.
            # It adds the the line height on each pass through the loop
            # Once it is greater then the height supplied by context.get_height
            # it marks the line and sets the current page height back to 0
            print "page_height ", page_height
            if page_height + line_height > height:
                page_breaks.append(line)
                page_height = 0
                page_height += line_height

        operation.set_n_pages(len(page_breaks) + 1)
        self.page_breaks = page_breaks

    def draw_page (self, operation, context, page_number):
        assert isinstance(self.page_breaks, list)
        #print page_number
        if page_number == 0:
            start = 0
        else:
            start = self.page_breaks[page_number - 1]

        try:
            end = self.page_breaks[page_number]
        except IndexError:
            end = self.layout.get_line_count()
        
        cr = context.get_cairo_context()

        cr.set_source_rgb(0, 0, 0)
        
        i = 0
        start_pos = 0
        iter = self.layout.get_iter()
        while 1:
            if i >= start:
                line = iter.get_line()
                _, logical_rect = iter.get_line_extents()
                x_bearing, y_bearing, lwidth, lheight = logical_rect
                baseline = iter.get_baseline()
                if i == start:
                    start_pos = y_bearing / 1024.0 # 1024.0 is float(pango.SCALE)
                cr.move_to(x_bearing / 1024.0, baseline / 1024.0 - start_pos)
                cr.show_layout_line(line)
            i += 1
            if not (i < end and iter.next_line()):
                break

def on_print_preview(widget=None):
    """
    Show the print preview.
    """
    global print_text
    action = gtk.PRINT_OPERATION_ACTION_PREVIEW
    printer = PrintExample(action, print_text)

def on_print_export(widget=None):
    """
    Export to a file. This requires the "export-filename" property to be set.
    """
    print "on_print_export"
    global print_text
    action = gtk.PRINT_OPERATION_ACTION_EXPORT
    printer = PrintExample(action, print_text, "MyPDFDocument.pdf")

def on_print_dialog(widget=None):
    """
    Show the print dialog.
    """
    global print_text
    action = gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG
    printer = PrintExample(action, print_text)

def on_print_immediately(widget=None):
    """
    Start printing immediately without showing the print dialog.
    Based on the current print settings.
    """
    global print_text
    action = gtk.PRINT_OPERATION_ACTION_PRINT
    printer = PrintExample(action, print_text)

def on_file_selected(widget=None):
    global print_text
    data=""
    file = open(widget.get_filename(), "r")
    for x in file.readlines():
        data = data + x
    file.close()
    print_text=data

def main():
    """
    PyGTK GUI to test gnome printing technologies
    """
    data=None
    win = gtk.Window()

    win.connect("delete_event", lambda w,e: gtk.main_quit())
    
    vbox = gtk.VBox(False, 0)
    hbox = gtk.HBox(False, 0)
    
    button_open = gtk.FileChooserButton("Open File")
    button_open.connect("selection-changed", on_file_selected)
    
    print_preview = gtk.Button("Print Preview")
    print_preview.connect("clicked", on_print_preview)

    print_immediately = gtk.Button("Print Immediately")
    print_immediately.connect("clicked", on_print_immediately)

    print_export = gtk.Button("Export to PDF")
    print_export.connect("clicked", on_print_export)

    print_dialog = gtk.Button("Print Dialog")
    print_dialog.connect("clicked", on_print_dialog)

    hbox.pack_start(print_dialog, True, True, 5)
    hbox.pack_start(print_immediately, True, True, 5)
    hbox.pack_start(print_export, True, True, 5)
    hbox.pack_start(print_preview, True, True, 5)
    vbox.pack_start(button_open, False, True, 5)
    vbox.pack_start(hbox, False, True, 5)

    win.add(vbox)
    win.show_all()

if __name__ == '__main__':
    main()
    gtk.main()
    
