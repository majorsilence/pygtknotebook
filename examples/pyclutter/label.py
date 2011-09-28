import clutter

stage = clutter.Stage()
stage.set_size(400, 400)

label = clutter.Text()
label.set_editable(False)
label.set_text("Clutter Label Text")
label.set_color(clutter.color_from_string("brown"))
# If no position is given it defaults to the upper most left corner.

stage.add(label)
stage.show_all()
stage.connect('destroy', clutter.main_quit)

clutter.main()
