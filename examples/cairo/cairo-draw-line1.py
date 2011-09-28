import cairo

WIDTH, HEIGHT = 400, 400

# Setup Cairo
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
context = cairo.Context(surface)

# Set thickness of brush
context.set_line_width(15)

# Draw Vertical Line
context.move_to(200, 150)
context.line_to(200, 250)

# Draw horizontal line
context.move_to(150, 200)
context.line_to(250, 200)
context.stroke()


# Output a PNG file
surface.write_to_png("cairo-draw-line1.png")
