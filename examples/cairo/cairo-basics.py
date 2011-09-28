#!/usr/bin/env python

import cairo
import math

def draw_rectangle(context=None):
    if context==None:
        return None
    # Y axis starts from top most part of surface
    # X starts left most of surface
    x1, y1 = 25, 150 # top left corner
    x2, y2 = 25, 250 # bottom left corner
    x3, y3 = 125, 250 # bottom right corner
    x4, y4 = 125, 150 # to
    
    context.set_source_rgb(1.0, 0.0, 0.0) # red
    context.move_to(x1, y1)
    context.line_to(x2, y2)
    context.line_to(x3, y3)
    context.line_to(x4, y4)
    # close_path() will draw the last line. This line is drawn from the last position to the first position.
    # So above that would draw a line from (x4, y4) to (x1, y1) thus completing the rectangle.
    context.close_path()
    
    # Apply the ink
    context.stroke()
        
def draw_triangle(context=None):
    if context==None:
        return None
    
    context.set_source_rgb(0.0, 1.0, 0.0) # green
    # Draw out the triangle using absolute coordinates
    context.move_to(275, 175)
    context.line_to(375, 375) # Draw based on absolute position
    context.rel_line_to(-200, 0) # Draw last line relative to current position
    context.close_path()
    
    # Apply the ink
    context.stroke()

def draw_circle(context=None):
    if context==None:
        return None

    width, height = 100, 100
    radius = min(width, height)
    
    context.set_source_rgb(0.0, 0.0, 1.0) # blue

    #context.arc(x, y, radius, start_angle, stop_angle)
    #angle in: radians=degree*(math.pi/180)
    context.arc(275, 100, radius / 2.0 - 20, 0, 2 * math.pi)
    context.stroke()
    
def draw_curve(context=None):
    if context==None:
        return None
    
    context.set_source_rgb(0.5, 0.0, 0.3)
    # curve_to(x1, y1, x2, y2, x3, y3)
    # if no current position is set, then x1 and y1 are set as the starting position
    context.move_to(20, 20)
    context.curve_to (60, 100, 100, 20, 140, 100)
    context.stroke() 


def main():
    WIDTH, HEIGHT = 400, 400

    # Setup Cairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    #surface = cairo.PDFSurface("drawings.pdf", WIDTH, HEIGHT)
    #surface = cairo.SVGSurface("drawings.svg", WIDTH, HEIGHT)
    context = cairo.Context(surface)

    # Set thickness of brush
    context.set_line_width(15)
    
    draw_rectangle(context)
    draw_triangle(context)
    draw_circle(context)
    draw_curve(context)

    # Output a PNG file
    surface.write_to_png("cairo-basics.png")

if __name__ == "__main__":
    main()
    

