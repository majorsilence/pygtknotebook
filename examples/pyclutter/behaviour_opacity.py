import clutter

class Blinker:
    def __init__(self):
        # Create a stage and with a clor se to red
        # and title of "My Blinking Rectangle Example'
        self.stage = clutter.Stage()
        self.stage.set_color(clutter.color_from_string("red"))
        self.stage.set_size(400, 400)
        self.stage.set_title('My Blinking Rectangle Example')

        self.rect = clutter.Rectangle()
        self.rect.set_color(clutter.color_from_string("green"))
        self.rect.set_size(200, 200)

        rect_xpos = self.stage.get_width() / 4
        rect_ypos = self.stage.get_height() / 4

        self.rect.set_position(rect_xpos, rect_ypos)

        # Create a time line with 30 frames per second and
        # 10 frames
        self.timeline = clutter.Timeline(duration=3000)

        # Set the timeline to loop forever
        self.timeline.set_loop(True)

        # Create a behaviour for the Green rectangle.
        #  Create an alpha channel and add it to a behaviour
        # and apply the behaviour to our Rectangle.
        # Not sure what clutter.ramp_func does
        # Sets the the up an alpha to the clutter timeline.
        alpha = clutter.Alpha(self.timeline, clutter.EASE_IN_OUT_QUART)
        # Sets the Opacity of alpha object we created above. 
        self.behaviour = clutter.BehaviourOpacity(alpha=alpha , opacity_start=0xdd, opacity_end=0)
        # Apply the behaviour and timeline to our Rectangle that was created above
        self.behaviour.apply(self.rect)

        # start the timeline running
        self.timeline.start()

        self.stage.add(self.rect)
        self.stage.show_all()
        self.stage.connect('destroy', clutter.main_quit)

if __name__ == "__main__":
    app = Blinker()
    clutter.main()
