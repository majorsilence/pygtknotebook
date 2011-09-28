import cairo      
  
# These are destination Surfaces
# all of them can be found at: http://www.cairographics.org/manual/Surfaces.html
#cairo.ImageSurface(format, width, height)
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT) 
surface = cairo.PDFSurface("drawings.pdf", WIDTH, HEIGHT)    
surface = cairo.SVGSurface("drawings.svg", WIDTH, HEIGHT)   
# FORMATS
#'FORMAT_A1', 'FORMAT_A8', 'FORMAT_ARGB32', 'FORMAT_RGB16_565', 'FORMAT_RGB24'


#context.set_source_rgb(Red, Green, Blue)
context.set_source_rgb(1.0, 1.0, 1.0)
#context.rectangle(x, y, width, height)
context.rectangle(10, 10, width - 20, height - 20)
context.fill()


# Line relative to the current position
#context.rel_line_to(x, y)

# Move relative to the current position
#context.rel_move_to(x, y)


