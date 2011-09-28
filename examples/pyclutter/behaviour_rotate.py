import clutter

stage = clutter.Stage()
stage.set_size(400, 400)

rect = clutter.Rectangle()
rect.set_color(clutter.color_from_string("red"))
rect.set_size(100, 100)
rect.set_position(150, 150)

timeline = clutter.Timeline(duration=3000)
timeline.set_loop(True)
alpha = clutter.Alpha(timeline, clutter.EASE_IN_OUT_SINE)

rotate_behaviour = clutter.BehaviourRotate(axis=clutter.Z_AXIS, angle_start=0.0, angle_end=359.0)
rotate_behaviour.set_alpha(alpha)
rotate_behaviour.apply(rect)

timeline.start()

stage.add(rect)
stage.show_all()
stage.connect('destroy', clutter.main_quit)

clutter.main()

