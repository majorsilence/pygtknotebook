import clutter

def create_texture(fName):
    image = clutter.Texture(filename=fName)
    (width, height) = image.get_size()

    return image

stage = clutter.Stage()
stage.set_size(400, 400)

# Create the original Texture from a picture of a flower
purple_flower = create_texture("flower.jpg")

# Create a clone of the origial Texture
cloned_flower = clutter.CloneTexture(purple_flower)
cloned_flower.set_position(200, 200)

stage.add(purple_flower, cloned_flower)
stage.show_all()
stage.connect('destroy', clutter.main_quit)

clutter.main()

