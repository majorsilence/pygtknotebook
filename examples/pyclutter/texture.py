import clutter
import gtk

stage = clutter.Stage()
stage.set_size(400, 400)

purple_flower = clutter.Texture(filename="flower.jpg")
(width, height) = purple_flower.get_size()

stage.add(purple_flower)
stage.show_all()
stage.connect('destroy', clutter.main_quit)

clutter.main()

