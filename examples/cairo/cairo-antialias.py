import cairo
import math

def draw_circle(context, xc, yc):
    radius = 150
    context.set_source_rgb(0.0, 0.0, 1.0)

    context.arc(xc, yc, radius / 2.0 - 20, 0, 2 * math.pi)
    context.stroke()
    
if __name__ == "__main__":  
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 300, 200)
    context = cairo.Context(surface)
    
    # Set thickness of brush
    context.set_line_width(20)

    draw_circle(context, 75, 100)
    #Turn off antialias
    context.set_antialias(cairo.ANTIALIAS_NONE)
    draw_circle(context, 225, 100)

    # Output a PNG file
    surface.write_to_png("cairo-antialias.png")
