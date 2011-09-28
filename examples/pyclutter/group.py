import clutter

class GroupExample:
    def __init__(self):
        stage = clutter.Stage()
        stage.set_size(400, 400)
        stage.set_color(clutter.color_parse("#FFFFFF"))

        rect1 = clutter.Rectangle()
        rect2 = clutter.Rectangle()

        group1 = clutter.Group()
        group2 = clutter.Group() 

        group1.add(rect1, group2)
        group2.add(rect2)

        group1.set_position(75, 75)
        group2.set_position(75, 75)

        rect1.set_position(0, 0)
        rect2.set_position(0, 0)

        rect1.set_size(200, 200)
        rect2.set_size(200, 200)

        rect1.set_color(clutter.color_parse("red"))
        rect2.set_color(clutter.color_parse("blue"))

        stage.add(group1)

        stage.show_all()
        stage.connect('destroy', clutter.main_quit)
        group1.show_all()
        group2.show_all()

if __name__ == '__main__':
    GroupExample()
    clutter.main()

