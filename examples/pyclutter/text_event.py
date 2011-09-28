import clutter

class EntryExample:
    def __init__(self):
        self.stage = clutter.Stage()
        self.stage.set_size(400, 400)
        self.stage.set_color(clutter.color_from_string("red"))

        self.text = clutter.Text()
        self.text.set_text("Text Entry")
        self.text.set_color(clutter.color_parse("green"))
        self.text.set_size(150, 50)
        self.text.set_position(200, 200)
        self.text.set_reactive(True)
        self.text.set_editable(True)

        self.text.connect("button-press-event", self.on_mouse_press_event)
        self.text.connect("key-press-event", self.on_key_press_event)
        self.stage.connect('destroy', clutter.main_quit)

        self.stage.add(self.text)        
        self.stage.show_all()

    def on_mouse_press_event(self, actor, event):
        # acquire key focus
        self.stage.set_key_focus(self.text)
        return False

    def on_key_press_event(self, actor, event):

        print "Text Actor is: ", actor.get_text()
        print "Key pressed is: ", unichr(event.keyval)

        

if __name__ == "__main__":
    app = EntryExample()
    clutter.main()
