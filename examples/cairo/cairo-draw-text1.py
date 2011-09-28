import cairo

text = "Hello to the Great Text."

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 75)
context = cairo.Context(surface)

context.set_source_rgb(0.0, 0.0, 0.0) # set to black
context.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
context.set_font_size(50)

# To retrieve information about the text you can use the following
x_bearing, y_bearing, width, height = context.text_extents(text)[:4]
print height

context.move_to(5, height)
context.show_text(text)
context.stroke()

surface.write_to_png("cairo-draw-text1.png")
