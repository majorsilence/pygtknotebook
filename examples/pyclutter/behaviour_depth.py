import clutter

stage = clutter.Stage()
stage.set_size(400, 400)

rect = clutter.Rectangle()
rect.set_color(clutter.color_from_string("red"))
rect.set_size(100, 100)
rect.set_position(150, 150)

timeline = clutter.Timeline(duration=6000)
timeline.set_loop(True)
alpha = clutter.Alpha(timeline, clutter.EASE_OUT_BOUNCE)

rotate_behaviour = clutter.BehaviourDepth(0, 250)
rotate_behaviour.set_alpha(alpha)
rotate_behaviour.apply(rect)

timeline.start()

stage.add(rect)
stage.show_all()
stage.connect('destroy', clutter.main_quit)

clutter.main()

